import { randomBytes } from "node:crypto";
import { NextResponse, type NextRequest } from "next/server";
import { guard } from "@/lib/edit";
import { putMedia, storeMode } from "@/lib/store";

const MAX = 4_000_000;
const isWebp = (b: Buffer) => b.length > 12 && b.toString("ascii", 0, 4) === "RIFF" && b.toString("ascii", 8, 12) === "WEBP";

// Recebe uma imagem já otimizada no navegador (versão grande "f" + miniatura "t", em WebP) e grava cifrada.
export async function POST(req: NextRequest) {
  const user = await guard(req);
  if (typeof user !== "string") return user;
  if (storeMode() === "readonly") return NextResponse.json({ error: "Armazenamento de imagens não configurado." }, { status: 503 });
  const form = await req.formData().catch(() => null);
  const f = form?.get("f");
  const t = form?.get("t");
  if (!(f instanceof Blob) || !(t instanceof Blob)) return NextResponse.json({ error: "envio inválido" }, { status: 400 });
  if (f.size > MAX || t.size > MAX) return NextResponse.json({ error: "imagem grande demais" }, { status: 413 });
  const full = Buffer.from(await f.arrayBuffer());
  const thumb = Buffer.from(await t.arrayBuffer());
  if (!isWebp(full) || !isWebp(thumb)) return NextResponse.json({ error: "formato inválido" }, { status: 400 });
  const id = randomBytes(8).toString("hex");
  await putMedia(id, "f", full);
  await putMedia(id, "t", thumb);
  return NextResponse.json({ id });
}
