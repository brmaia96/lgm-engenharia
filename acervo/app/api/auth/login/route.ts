import { NextResponse, type NextRequest } from "next/server";
import { checkPassword, clearFailures, rateLimited, registerFailure } from "@/lib/auth";
import { SESSION_COOKIE, SESSION_HOURS, signSession } from "@/lib/session";

export async function POST(req: NextRequest) {
  const ip = req.headers.get("x-forwarded-for")?.split(",")[0]?.trim() || "local";
  if (rateLimited(ip)) {
    return NextResponse.json({ error: "Muitas tentativas. Aguarde 15 minutos." }, { status: 429 });
  }
  // só aceita POST do próprio site
  const origin = req.headers.get("origin");
  if (origin && new URL(origin).host !== req.nextUrl.host) {
    return NextResponse.json({ error: "origem inválida" }, { status: 403 });
  }

  let body: { user?: unknown; password?: unknown };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "requisição inválida" }, { status: 400 });
  }
  const user = typeof body.user === "string" ? body.user.trim().toLowerCase().slice(0, 64) : "";
  const password = typeof body.password === "string" ? body.password.slice(0, 256) : "";

  if (!user || !password || !(await checkPassword(user, password))) {
    registerFailure(ip);
    await new Promise((r) => setTimeout(r, 400));
    return NextResponse.json({ error: "Usuário ou senha incorretos." }, { status: 401 });
  }

  clearFailures(ip);
  const res = NextResponse.json({ ok: true });
  res.cookies.set(SESSION_COOKIE, await signSession(user), {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    maxAge: SESSION_HOURS * 3600,
  });
  return res;
}
