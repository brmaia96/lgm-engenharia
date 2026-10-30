import { NextResponse, type NextRequest } from "next/server";
import { applyEdit, currentRev, guard, persist, type EditPayload } from "@/lib/edit";
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
    const p = await applyEdit(code, body, user);
    return persist([p], user, Number(body.rev));
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
  return persist([next], user, await currentRev());
}
