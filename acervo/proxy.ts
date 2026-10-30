import { NextResponse, type NextRequest } from "next/server";
import { SESSION_COOKIE, verifySession } from "@/lib/session";

// Portão de acesso: tudo exige sessão válida, exceto a tela de login e os arquivos de marca.
const PUBLIC = ["/login", "/api/auth/login"];

export async function proxy(req: NextRequest) {
  const { pathname, search } = req.nextUrl;
  if (PUBLIC.includes(pathname)) return NextResponse.next();

  const user = await verifySession(req.cookies.get(SESSION_COOKIE)?.value);
  if (user) {
    // /api/m/<id>/<t|f> → rota da fatia correspondente (/api/m<1º caractere>/…)
    const m = pathname.match(/^\/api\/m\/([0-9a-f])([0-9a-f]{15})\/([tf])$/);
    if (m) {
      const url = req.nextUrl.clone();
      url.pathname = `/api/m${m[1]}/${m[1]}${m[2]}/${m[3]}`;
      return NextResponse.rewrite(url);
    }
    return NextResponse.next();
  }

  if (pathname.startsWith("/api/")) {
    return NextResponse.json({ error: "não autorizado" }, { status: 401 });
  }
  const url = req.nextUrl.clone();
  url.pathname = "/login";
  url.search = pathname === "/" ? "" : `?next=${encodeURIComponent(pathname + search)}`;
  return NextResponse.redirect(url);
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|brand/|favicon.ico|icon.svg|robots.txt).*)"],
};
