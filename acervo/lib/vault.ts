import "server-only";
import { createDecipheriv } from "node:crypto";
import { readFile } from "node:fs/promises";
import path from "node:path";
import type { Catalogo, Projeto, ProjetoResumo } from "./types";

// Formato de cada arquivo .enc: [12 bytes IV][16 bytes auth tag][ciphertext] — AES-256-GCM.
// O repositório só guarda ciphertext; a chave existe apenas na variável VAULT_KEY do servidor.

const VAULT_DIR = path.join(process.cwd(), "vault");

export function vaultKey(): Buffer {
  const raw = process.env.VAULT_KEY;
  if (!raw) throw new Error("VAULT_KEY ausente");
  const k = Buffer.from(raw, "base64");
  if (k.length !== 32) throw new Error("VAULT_KEY deve ter 32 bytes em base64");
  return k;
}

export function decrypt(buf: Buffer): Buffer {
  const iv = buf.subarray(0, 12);
  const tag = buf.subarray(12, 28);
  const d = createDecipheriv("aes-256-gcm", vaultKey(), iv);
  d.setAuthTag(tag);
  return Buffer.concat([d.update(buf.subarray(28)), d.final()]);
}

// o cofre do repositório não muda durante a vida da instância
let base: Catalogo | null = null;

export async function getBaseCatalog(): Promise<Catalogo> {
  if (base) return base;
  try {
    const buf = await readFile(path.join(VAULT_DIR, "catalog.enc"));
    base = JSON.parse(decrypt(buf).toString("utf8")) as Catalogo;
  } catch (e) {
    if ((e as NodeJS.ErrnoException).code !== "ENOENT") throw e;
    base = { version: 1, updated: new Date(0).toISOString(), projects: [] };
  }
  return base;
}

export async function getLog() {
  const { readOverlay } = await import("./store");
  return (await readOverlay()).log ?? [];
}

export interface Acervo {
  /** projetos ativos (fora da lixeira) */
  projects: Projeto[];
  /** projetos na lixeira */
  trash: Projeto[];
  /** revisão das edições feitas pelo site (para detectar conflito ao salvar) */
  rev: number;
}

/** Cofre do repositório + edições feitas pelo site. */
export async function getAcervo(): Promise<Acervo> {
  const { readOverlay } = await import("./store");
  const [b, overlay] = await Promise.all([getBaseCatalog(), readOverlay()]);
  const baseCodes = new Set(b.projects.map((p) => p.code));
  const all = [
    ...b.projects.map((p) => overlay.projects[p.code] ?? p),
    // projetos criados pelo site
    ...Object.values(overlay.projects).filter((p) => !baseCodes.has(p.code)),
  ];
  return {
    projects: all.filter((p) => !p.lixeira),
    trash: all.filter((p) => p.lixeira),
    rev: overlay.rev,
  };
}

/** projeto (ativo ou na lixeira) */
export async function getProject(code: string): Promise<Projeto | undefined> {
  const { projects, trash } = await getAcervo();
  return [...projects, ...trash].find((p) => p.code.toLowerCase() === code.toLowerCase());
}

export async function getBaseProject(code: string): Promise<Projeto | undefined> {
  return (await getBaseCatalog()).projects.find((p) => p.code.toLowerCase() === code.toLowerCase());
}

export function summarize(p: Projeto): ProjetoResumo {
  const { media, ...rest } = p;
  const counts: ProjetoResumo["counts"] = {};
  for (const m of media) counts[m.cat] = (counts[m.cat] ?? 0) + 1;
  const cover = (p.cover && media.some((m) => m.id === p.cover) ? p.cover : undefined)
    ?? media.find((m) => m.cat === "fachada")?.id ?? media[0]?.id;
  const thumbs = [cover, ...media.filter((m) => m.id !== cover && (m.cat === "fachada" || m.cat === "interna")).map((m) => m.id)]
    .filter(Boolean)
    .slice(0, 4) as string[];
  return { ...rest, cover, counts, thumbs };
}

const ID_RE = /^[a-f0-9]{16}$/;

export async function readMedia(id: string, size: "t" | "f"): Promise<Buffer | null> {
  if (!ID_RE.test(id)) return null;
  try {
    const buf = await readFile(path.join(VAULT_DIR, "media", `${id}.${size}.enc`));
    return decrypt(buf);
  } catch {
    // imagem enviada pelo site (fora do cofre do repositório)
    const { getMedia } = await import("./store");
    return getMedia(id, size);
  }
}
