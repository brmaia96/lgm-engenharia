import { NextResponse, type NextRequest } from "next/server";
import { currentRev, guard, persist } from "@/lib/edit";
import { getProject } from "@/lib/vault";

export async function POST(req: NextRequest, ctx: RouteContext<"/api/projetos/[code]/restaurar">) {
  const user = await guard(req);
  if (typeof user !== "string") return user;
  const { code } = await ctx.params;
  const p = await getProject(code);
  if (!p) return NextResponse.json({ error: "projeto não encontrado" }, { status: 404 });
  const { lixeira: _removido, ...rest } = p;
  return persist([{ project: { ...rest, editado: { em: new Date().toISOString(), por: user } }, acao: "restaurou", mudancas: [] }], user, await currentRev());
}
