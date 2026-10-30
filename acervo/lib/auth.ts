import "server-only";
import { scrypt, timingSafeEqual } from "node:crypto";
import { cookies } from "next/headers";
import { parseUsers, SESSION_COOKIE, verifySession } from "./session";

// Hash no formato scrypt.N.r.p.salt(b64).hash(b64) — gerado por `npm run acervo:user`.
function scryptAsync(pw: string, salt: Buffer, len: number, N: number, r: number, p: number) {
  return new Promise<Buffer>((resolve, reject) =>
    scrypt(pw, salt, len, { N, r, p, maxmem: 256 * N * r }, (err, key) => (err ? reject(err) : resolve(key))),
  );
}

// hash fictício para gastar o mesmo tempo quando o usuário não existe
const DUMMY = "scrypt.16384.8.1.AAAAAAAAAAAAAAAAAAAAAA==.AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";

export async function checkPassword(user: string, password: string): Promise<boolean> {
  const stored = parseUsers().get(user.trim().toLowerCase());
  const [alg, N, r, p, saltB64, hashB64] = (stored ?? DUMMY).split(".");
  if (alg !== "scrypt") return false;
  const expected = Buffer.from(hashB64, "base64");
  const got = await scryptAsync(password, Buffer.from(saltB64, "base64"), expected.length, +N, +r, +p);
  return Boolean(stored) && got.length === expected.length && timingSafeEqual(got, expected);
}

export async function currentUser(): Promise<string | null> {
  const jar = await cookies();
  return verifySession(jar.get(SESSION_COOKIE)?.value);
}

// Limite de tentativas por IP (melhor esforço — memória da instância).
const attempts = new Map<string, { n: number; until: number }>();
const MAX = 6;
const WINDOW = 15 * 60_000;

export function rateLimited(ip: string) {
  const a = attempts.get(ip);
  return Boolean(a && a.n >= MAX && Date.now() < a.until);
}

export function registerFailure(ip: string) {
  const a = attempts.get(ip);
  if (!a || Date.now() > a.until) attempts.set(ip, { n: 1, until: Date.now() + WINDOW });
  else a.n++;
}

export function clearFailures(ip: string) {
  attempts.delete(ip);
}
