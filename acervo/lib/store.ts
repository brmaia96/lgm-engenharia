import "server-only";
import { createCipheriv, randomBytes } from "node:crypto";
import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import type { Projeto } from "./types";
import { decrypt, vaultKey } from "./vault";

// Camada de edições feitas pelo site. O cofre do repositório (vault/) é somente leitura;
// cada salvamento grava uma NOVA revisão cifrada (overlay-00000042.enc) com a versão
// completa dos projetos alterados. Ler = pegar a revisão mais recente. Isso dá histórico
// e evita sobrescrever o trabalho do outro usuário (conflito de revisão).
//
// Armazenamento: Vercel Blob privado (BLOB_READ_WRITE_TOKEN) em produção;
// pasta local .data/ em desenvolvimento.

export interface Mudanca {
  campo: string;
  de?: string;
  para?: string;
}

export interface Registro {
  em: string;
  por: string;
  acao: "criou" | "editou" | "excluiu" | "restaurou";
  code: string;
  titulo: string;
  mudancas: Mudanca[];
}

export interface Overlay {
  rev: number;
  updatedAt: string;
  by: string;
  projects: Record<string, Projeto>;
  /** histórico de alterações, mais recente primeiro */
  log?: Registro[];
}

export interface Alteracao {
  project: Projeto;
  acao: Registro["acao"];
  mudancas: Mudanca[];
}

const EMPTY: Overlay = { rev: 0, updatedAt: new Date(0).toISOString(), by: "", projects: {}, log: [] };
const LOG_MAX = 5000;
const PREFIX = "acervo/overlay-";
const LOCAL_DIR = path.join(process.cwd(), ".data");
const KEEP = 60;

export class ConflictError extends Error {}

export function storeMode(): "blob" | "local" | "readonly" {
  if (process.env.BLOB_READ_WRITE_TOKEN) return "blob";
  if (process.env.NODE_ENV !== "production" || process.env.ACERVO_LOCAL_STORE === "1") return "local";
  return "readonly";
}

function encrypt(buf: Buffer) {
  const iv = randomBytes(12);
  const c = createCipheriv("aes-256-gcm", vaultKey(), iv);
  const ct = Buffer.concat([c.update(buf), c.final()]);
  return Buffer.concat([iv, c.getAuthTag(), ct]);
}

const revName = (rev: number) => `${PREFIX}${String(rev).padStart(8, "0")}.enc`;

async function listRevs(): Promise<string[]> {
  const mode = storeMode();
  if (mode === "blob") {
    const { list } = await import("@vercel/blob");
    const names: string[] = [];
    let cursor: string | undefined;
    do {
      const r = await list({ prefix: PREFIX, cursor, limit: 1000 });
      names.push(...r.blobs.map((b) => b.pathname));
      cursor = r.hasMore ? r.cursor : undefined;
    } while (cursor);
    return names.sort();
  }
  if (mode === "local") {
    try {
      return (await readdir(path.join(LOCAL_DIR, "acervo")))
        .map((f) => `acervo/${f}`)
        .filter((n) => n.startsWith(PREFIX))
        .sort();
    } catch {
      return [];
    }
  }
  return [];
}

async function readRev(name: string): Promise<Buffer> {
  if (storeMode() === "blob") {
    const { get } = await import("@vercel/blob");
    const r = await get(name, { access: "private", useCache: false });
    if (!r || r.statusCode !== 200) throw new Error(`revisão ${name} indisponível`);
    return Buffer.from(await new Response(r.stream).arrayBuffer());
  }
  return readFile(path.join(LOCAL_DIR, name));
}

async function writeRev(name: string, data: Buffer) {
  if (storeMode() === "blob") {
    const { put } = await import("@vercel/blob");
    try {
      await put(name, data, { access: "private", addRandomSuffix: false, allowOverwrite: false, contentType: "application/octet-stream" });
    } catch (e) {
      if (/already exists/i.test(String(e))) throw new ConflictError("revisão já existe");
      throw e;
    }
    return;
  }
  const file = path.join(LOCAL_DIR, name);
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, data, { flag: "wx" }).catch((e) => {
    if (e.code === "EEXIST") throw new ConflictError("revisão já existe");
    throw e;
  });
}

// revisões são imutáveis: guarda a última decifrada e só baixa de novo se surgir outra
let cache: { name: string; data: Overlay } | null = null;

export async function readOverlay(): Promise<Overlay> {
  if (storeMode() === "readonly") return EMPTY;
  const last = (await listRevs()).at(-1);
  if (!last) return EMPTY;
  if (cache?.name === last) return cache.data;
  const data = JSON.parse(decrypt(await readRev(last)).toString("utf8")) as Overlay;
  cache = { name: last, data };
  return data;
}

/** Grava uma nova revisão com os projetos alterados. Recusa se outra revisão entrou no meio. */
export async function saveProjects(changes: Alteracao[], by: string, baseRev: number): Promise<Overlay> {
  if (storeMode() === "readonly") throw new Error("Armazenamento de edições não configurado (BLOB_READ_WRITE_TOKEN).");
  const current = await readOverlay();
  if (current.rev !== baseRev) throw new ConflictError("O acervo foi alterado por outra pessoa. Recarregue a página.");
  const next: Overlay = {
    rev: current.rev + 1,
    updatedAt: new Date().toISOString(),
    by,
    projects: { ...current.projects },
    log: [
      ...changes.map((c) => ({ em: new Date().toISOString(), por: by, acao: c.acao, code: c.project.code, titulo: c.project.titulo, mudancas: c.mudancas })),
      ...(current.log ?? []),
    ].slice(0, LOG_MAX),
  };
  for (const c of changes) next.projects[c.project.code] = c.project;
  await writeRev(revName(next.rev), encrypt(Buffer.from(JSON.stringify(next))));
  cache = { name: revName(next.rev), data: next };
  void prune();
  return next;
}

async function prune() {
  try {
    const revs = await listRevs();
    const old = revs.slice(0, Math.max(0, revs.length - KEEP));
    if (!old.length) return;
    if (storeMode() === "blob") {
      const { del } = await import("@vercel/blob");
      await del(old);
    }
  } catch {
    // limpeza é opcional
  }
}

// ---------- imagens enviadas pelo site ----------
const mediaName = (id: string, size: "t" | "f") => `acervo/media/${id}.${size}.enc`;

export async function putMedia(id: string, size: "t" | "f", data: Buffer) {
  const enc = encrypt(data);
  if (storeMode() === "blob") {
    const { put } = await import("@vercel/blob");
    await put(mediaName(id, size), enc, { access: "private", addRandomSuffix: false, allowOverwrite: false, contentType: "application/octet-stream" });
    return;
  }
  if (storeMode() === "readonly") throw new Error("Armazenamento não configurado (BLOB_READ_WRITE_TOKEN).");
  const file = path.join(LOCAL_DIR, mediaName(id, size));
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, enc);
}

export async function getMedia(id: string, size: "t" | "f"): Promise<Buffer | null> {
  try {
    if (storeMode() === "blob") {
      const { get } = await import("@vercel/blob");
      const r = await get(mediaName(id, size), { access: "private" });
      if (!r || r.statusCode !== 200) return null;
      return decrypt(Buffer.from(await new Response(r.stream).arrayBuffer()));
    }
    if (storeMode() === "local") return decrypt(await readFile(path.join(LOCAL_DIR, mediaName(id, size))));
  } catch {
    return null;
  }
  return null;
}
