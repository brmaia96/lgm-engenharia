import { NextResponse, type NextRequest } from "next/server";
import { applyEdit, currentRev, diff, guard, persist, type EditPayload } from "@/lib/edit";
import { buildCode, buildName } from "@/lib/naming";
import type { Midia, Projeto } from "@/lib/types";
import { getAcervo } from "@/lib/vault";

// Cria um projeto novo pelo site. As imagens já foram enviadas para /api/midia.
export async function POST(req: NextRequest) {
  const user = await guard(req);
  if (typeof user !== "string") return user;
  let body: Omit<EditPayload, "media"> & { media?: { id: string; cat: Midia["cat"]; legenda?: string; w: number; h: number }[] };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "requisição inválida" }, { status: 400 });
  }
  const media = (body.media ?? []).filter((m) => /^[a-f0-9]{16}$/.test(m.id)).map((m) => ({ id: m.id, cat: m.cat, w: Math.round(Number(m.w) || 0), h: Math.round(Number(m.h) || 0) }));
  if (!media.length) return NextResponse.json({ error: "Envie pelo menos uma imagem." }, { status: 400 });
  const { projects, trash } = await getAcervo();
  const max = [...projects, ...trash].reduce((n, p) => Math.max(n, parseInt(p.code.slice(2), 10) || 0), 0);
  const code = buildCode(max + 1);
  const draft: Projeto = {
    code, name: "", tipo: "R", terreno: null, pavimentos: "ND", area: null, suites: null,
    titulo: "Novo projeto", media: media as Midia[], cover: media[0].id,
  };
  try {
    // aplica e valida os campos com a mesma regra da edição
    const p = await applyEdit(code, { ...body, rev: 0, media: media.map((m, i) => ({ id: m.id, cat: m.cat, legenda: body.media?.[i]?.legenda })) }, user, draft);
    p.name = buildName(p);
    return persist([{ project: p, acao: "criou", mudancas: diff(undefined, p) }], user, await currentRev());
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 400 });
  }
}
