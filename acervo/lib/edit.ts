import "server-only";
import { NextResponse, type NextRequest } from "next/server";
import { currentUser } from "./auth";
import { buildName, CATEGORIAS, PAVIMENTOS, TIPOS } from "./naming";
import { ConflictError, saveProjects, type Alteracao, type Mudanca } from "./store";
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
export async function applyEdit(code: string, body: EditPayload, user: string, draft?: Projeto): Promise<Projeto> {
  const cur = draft ?? (await getProject(code));
  const base = await getBaseProject(code);
  if (!cur) throw new Error("projeto não encontrado");
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
    const known = new Map([...(base?.media ?? []), ...(cur.retiradas ?? []), ...cur.media].map((m) => [m.id, m]));
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
    const ret = [...known.values()].filter((m) => !media.some((x) => x.id === m.id));
    p.retiradas = ret.length ? ret : undefined;
  }
  if (body.cover !== undefined) p.cover = body.cover;
  if (p.cover && !p.media.some((m) => m.id === p.cover)) p.cover = p.media.find((m) => m.cat === "fachada")?.id ?? p.media[0]?.id;

  p.name = buildName(p);
  p.editado = { em: new Date().toISOString(), por: user };
  return p;
}

export async function persist(changes: Alteracao[], user: string, rev: number) {
  try {
    const o = await saveProjects(changes, user, rev);
    return NextResponse.json({ ok: true, rev: o.rev, projects: changes.map((c) => ({ code: c.project.code, name: c.project.name })) });
  } catch (e) {
    if (e instanceof ConflictError) return NextResponse.json({ error: e.message }, { status: 409 });
    throw e;
  }
}

export async function currentRev() {
  return (await getAcervo()).rev;
}

// ---------- diferenças para o histórico ----------
const ROTULOS: Record<string, string> = {
  titulo: "Título", descricao: "Descrição", tipo: "Tipo", pavimentos: "Pavimentos", terreno: "Terreno", area: "Área",
  suites: "Suítes", quartos: "Dormitórios", banheiros: "Banheiros", vagas: "Vagas", piscina: "Piscina", gourmet: "Área gourmet",
  destaque: "Destaque", sistema: "Sistema", estilo: "Estilo", data: "Data", tags: "Etiquetas", name: "Nome padrão",
};

function show(k: string, v: unknown): string {
  if (v === undefined || v === null || v === "" || (Array.isArray(v) && !v.length)) return "—";
  if (k === "tipo") return TIPOS[v as Tipo] ?? String(v);
  if (k === "pavimentos") return PAVIMENTOS[v as Pavimento] ?? String(v);
  if (k === "terreno") return `${(v as { frente: number }).frente} x ${(v as { fundo: number }).fundo} m`;
  if (k === "area") return `${v} m²`;
  if (typeof v === "boolean") return v ? "Sim" : "Não";
  if (Array.isArray(v)) return v.join(", ");
  const s = String(v);
  return s.length > 140 ? s.slice(0, 137) + "…" : s;
}

export function diff(a: Projeto | undefined, b: Projeto): Mudanca[] {
  if (!a) return [{ campo: "Projeto", para: `${b.code} criado com ${b.media.length} imagens` }];
  const out: Mudanca[] = [];
  for (const k of Object.keys(ROTULOS) as (keyof Projeto)[]) {
    const x = show(k, a[k]);
    const y = show(k, b[k]);
    if (x !== y) out.push({ campo: ROTULOS[k], de: x, para: y });
  }
  const ida = a.media.map((m) => m.id);
  const idb = b.media.map((m) => m.id);
  const tiradas = ida.filter((i) => !idb.includes(i)).length;
  const voltaram = idb.filter((i) => !ida.includes(i)).length;
  if (tiradas) out.push({ campo: "Imagens", para: `${tiradas} retirada(s)` });
  if (voltaram) out.push({ campo: "Imagens", para: `${voltaram} adicionada(s)` });
  const cats = b.media.filter((m) => { const o = a.media.find((x) => x.id === m.id); return o && o.cat !== m.cat; }).length;
  if (cats) out.push({ campo: "Imagens", para: `${cats} mudaram de categoria` });
  const legs = b.media.filter((m) => { const o = a.media.find((x) => x.id === m.id); return o && (o.legenda ?? "") !== (m.legenda ?? ""); }).length;
  if (legs) out.push({ campo: "Imagens", para: `${legs} legenda(s) alterada(s)` });
  const common = idb.filter((i) => ida.includes(i));
  if (common.join() !== ida.filter((i) => idb.includes(i)).join()) out.push({ campo: "Imagens", para: "ordem alterada" });
  if ((a.cover ?? "") !== (b.cover ?? "")) out.push({ campo: "Capa", para: "trocada" });
  return out;
}
