// Sessão em JWT assinado (HS256) num cookie httpOnly. Usado pelo proxy e pelas rotas.
import { jwtVerify, SignJWT } from "jose";

export const SESSION_COOKIE = "cb_session";
export const SESSION_HOURS = 12;

function secret() {
  const s = process.env.AUTH_SECRET;
  if (!s || s.length < 32) throw new Error("AUTH_SECRET ausente ou curto (mín. 32 caracteres)");
  return new TextEncoder().encode(s);
}

export async function signSession(user: string) {
  return new SignJWT({ sub: user })
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime(`${SESSION_HOURS}h`)
    .setIssuer("cobogo-acervo")
    .sign(secret());
}

export async function verifySession(token: string | undefined): Promise<string | null> {
  if (!token) return null;
  try {
    const { payload } = await jwtVerify(token, secret(), { issuer: "cobogo-acervo", algorithms: ["HS256"] });
    const user = typeof payload.sub === "string" ? payload.sub : null;
    // usuário removido de AUTH_USERS perde o acesso imediatamente
    return user && userNames().includes(user) ? user : null;
  } catch {
    return null;
  }
}

/** AUTH_USERS = "maia:scrypt.<...>;rafael:scrypt.<...>" */
export function parseUsers(): Map<string, string> {
  const map = new Map<string, string>();
  for (const entry of (process.env.AUTH_USERS ?? "").split(";")) {
    const i = entry.indexOf(":");
    if (i > 0) map.set(entry.slice(0, i).trim().toLowerCase(), entry.slice(i + 1).trim());
  }
  return map;
}

export function userNames() {
  return [...parseUsers().keys()];
}
