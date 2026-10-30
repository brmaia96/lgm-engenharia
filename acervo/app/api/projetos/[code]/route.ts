import { NextResponse, type NextRequest } from "next/server";
import { applyEdit, currentRev, diff, guard, persist, type EditPayload } from "@/lib/edit";
import { getProject } from "@/lib/vault";

// PATCH = salvar edição · DELETE = mover para a lixeira (dá para restaurar)
export async function PATCH(req: NextRequest, ctx: RouteContext<"/api/projetos/[code]">) {
  const user = await guard(req);
  if (typeof user !== "string") return user;
  const { code } = await ctx.params;
  let body: EditPayload;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "requisição inválida" }, { status: 400 });
  }
  try {
    const before = await getProject(code);
    const p = await applyEdit(code, body, user);
    const mudancas = diff(before, p);
    if (!mudancas.length) return NextResponse.json({ ok: true, unchanged: true });
    return persist([{ project: p, acao: "editou", mudancas }], user, Number(body.rev));
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 400 });
  }
}

export async function DELETE(req: NextRequest, ctx: RouteContext<"/api/projetos/[code]">) {
  const user = await guard(req);
  if (typeof user !== "string") return user;
  const { code } = await ctx.params;
  const { motivo } = (await req.json().catch(() => ({}))) as { motivo?: string };
  const p = await getProject(code);
  if (!p) return NextResponse.json({ error: "projeto não encontrado" }, { status: 404 });
  const next = {
    ...p,
    lixeira: { em: new Date().toISOString(), por: user, ...(motivo ? { motivo: String(motivo).slice(0, 200) } : {}) },
  };
  return persist([{ project: next, acao: "excluiu", mudancas: motivo ? [{ campo: "Motivo", para: String(motivo).slice(0, 200) }] : [] }], user, await currentRev());
}
