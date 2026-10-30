import "server-only";
import { createDecipheriv } from "node:crypto";
import { readFile } from "node:fs/promises";
import path from "node:path";
import type { Catalogo, Projeto, ProjetoResumo } from "./types";

// Formato de cada arquivo .enc: [12 bytes IV][16 bytes auth tag][ciphertext] — AES-256-GCM.
// O repositório só guarda ciphertext; a chave existe apenas na variável VAULT_KEY do servidor.

const VAULT_DIR = path.join(process.cwd(), "vault");

function key(): Buffer {
  const raw = process.env.VAULT_KEY;
  if (!raw) throw new Error("VAULT_KEY ausente");
  const k = Buffer.from(raw, "base64");
  if (k.length !== 32) throw new Error("VAULT_KEY deve ter 32 bytes em base64");
  return k;
}

export function decrypt(buf: Buffer): Buffer {
  const iv = buf.subarray(0, 12);
  const tag = buf.subarray(12, 28);
  const d = createDecipheriv("aes-256-gcm", key(), iv);
  d.setAuthTag(tag);
  return Buffer.concat([d.update(buf.subarray(28)), d.final()]);
}

let cache: { at: number; data: Catalogo } | null = null;

export async function getCatalog(): Promise<Catalogo> {
  if (cache && Date.now() - cache.at < 60_000) return cache.data;
  try {
    const buf = await readFile(path.join(VAULT_DIR, "catalog.enc"));
    const data = JSON.parse(decrypt(buf).toString("utf8")) as Catalogo;
    cache = { at: Date.now(), data };
    return data;
  } catch (e) {
    if ((e as NodeJS.ErrnoException).code === "ENOENT") {
      return { version: 1, updated: new Date(0).toISOString(), projects: [] };
    }
    throw e;
  }
}

export async function getProject(code: string): Promise<Projeto | undefined> {
  const c = await getCatalog();
  return c.projects.find((p) => p.code.toLowerCase() === code.toLowerCase());
}

export function summarize(p: Projeto): ProjetoResumo {
  const { media, ...rest } = p;
  const counts: ProjetoResumo["counts"] = {};
  for (const m of media) counts[m.cat] = (counts[m.cat] ?? 0) + 1;
  const cover = p.cover ?? media.find((m) => m.cat === "fachada")?.id ?? media[0]?.id;
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
    return null;
  }
}
