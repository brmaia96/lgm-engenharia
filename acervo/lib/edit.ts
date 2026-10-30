import "server-only";
import { NextResponse, type NextRequest } from "next/server";
import { currentUser } from "./auth";
import { buildName, CATEGORIAS, PAVIMENTOS, TIPOS } from "./naming";
import { ConflictError, saveProjects } from "./store";
import type { Categoria, Midia, Pavimento, Projeto, Tipo } from "./types";
import { getAcervo, getBaseProject, getProject } from "./vault";

/** Garante usuário logado e requisição vinda do próprio site (proteção CSRF). */
export async function guard(req: NextRequest): Promise<string | NextResponse> {
  const user = await currentUser();
  if (!user) return NextResponse.json({ error: "Sessão expirada. Entre novamente." }, { status: 401 });
  const origin = req.headers.get("origin");
  if (!origin || new URL(origin).host !== req.nextUrl.host) {
    return NextResponse.json({ error: "origem inválida" }, { status: 403 });
  }
  return user;
}

export type EditPayload = Partial<{
  titulo: string;
  descricao: string;
  tipo: Tipo;
  pavimentos: Pavimento;
  terreno: { frente: number; fundo: number } | null;
  area: number | null;
  suites: number | null;
  quartos: number | null;
  banheiros: number | null;
  vagas: number | null;
  piscina: boolean;
  gourmet: boolean;
  destaque: boolean;
  sistema: string;
  estilo: string;
  data: string;
  tags: string[];
  cover: string;
  media: { id: string; cat: Categoria; legenda?: string }[];
}> & { rev: number };

const str = (v: unknown, max = 300) => (typeof v === "string" ? v.trim().slice(0, max) : undefined);
const num = (v: unknown, int = false) => {
  if (v === null || v === "") return null;
  const n = typeof v === "number" ? v : Number(v);
  if (!Number.isFinite(n) || n < 0 || n > 1e6) throw new Error("número inválido");
  return int ? Math.round(n) : Math.round(n * 100) / 100;
};

/** Aplica as alterações sobre o projeto atual, validando tudo. */
export async function applyEdit(code: string, body: EditPayload, user: string): Promise<Projeto> {
  const cur = await getProject(code);
  const base = await getBaseProject(code);
  if (!cur || !base) throw new Error("projeto não encontrado");
  const p: Projeto = structuredClone(cur);

  const titulo = str(body.titulo, 140);
  if (titulo !== undefined) {
    if (!titulo) throw new Error("O título não pode ficar vazio.");
    p.titulo = titulo;
  }
  for (const k of ["descricao", "sistema", "estilo"] as const) {
    const v = str(body[k], k === "descricao" ? 2000 : 80);
    if (v !== undefined) p[k] = v || undefined;
  }
  if (body.data !== undefined) p.data = str(body.data, 7) || undefined;
  if (body.tipo !== undefined) {
    if (!(body.tipo in TIPOS)) throw new Error("tipo inválido");
    p.tipo = body.tipo;
  }
  if (body.pavimentos !== undefined) {
    if (!(body.pavimentos in PAVIMENTOS)) throw new Error("pavimentos inválido");
    p.pavimentos = body.pavimentos;
  }
  if (body.terreno !== undefined) {
    if (body.terreno === null) p.terreno = null;
    else {
      const frente = num(body.terreno.frente);
      const fundo = num(body.terreno.fundo);
      p.terreno = frente && fundo ? { frente, fundo } : null;
    }
  }
  if (body.area !== undefined) p.area = num(body.area);
  if (body.suites !== undefined) p.suites = num(body.suites, true);
  for (const k of ["quartos", "banheiros", "vagas"] as const) {
    if (body[k] !== undefined) p[k] = num(body[k], true) ?? undefined;
  }
  for (const k of ["piscina", "gourmet", "destaque"] as const) {
    if (body[k] !== undefined) p[k] = Boolean(body[k]) || undefined;
  }
  if (body.tags !== undefined) {
    p.tags = [...new Set(body.tags.map((t) => str(t, 40)).filter(Boolean) as string[])].slice(0, 20);
  }
  if (body.media !== undefined) {
    // só aceita imagens que existem no cofre deste projeto; a ordem enviada vira a ordem da galeria
    const known = new Map(base.media.map((m) => [m.id, m]));
    const seen = new Set<string>();
    const media: Midia[] = [];
    for (const m of body.media) {
      const orig = known.get(m.id);
      if (!orig || seen.has(m.id)) continue;
      if (!(m.cat in CATEGORIAS)) throw new Error("categoria inválida");
      seen.add(m.id);
      const legenda = str(m.legenda, 80);
      media.push({ ...orig, cat: m.cat, legenda: legenda || undefined });
    }
    p.media = media;
  }
  if (body.cover !== undefined) p.cover = body.cover;
  if (p.cover && !p.media.some((m) => m.id === p.cover)) p.cover = p.media.find((m) => m.cat === "fachada")?.id ?? p.media[0]?.id;

  p.name = buildName(p);
  p.editado = { em: new Date().toISOString(), por: user };
  return p;
}

export async function persist(projects: Projeto[], user: string, rev: number) {
  try {
    const o = await saveProjects(projects, user, rev);
    return NextResponse.json({ ok: true, rev: o.rev, projects: projects.map((p) => ({ code: p.code, name: p.name })) });
  } catch (e) {
    if (e instanceof ConflictError) return NextResponse.json({ error: e.message }, { status: 409 });
    throw e;
  }
}

export async function currentRev() {
  return (await getAcervo()).rev;
}
