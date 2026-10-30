import { NextResponse } from "next/server";
import { currentUser } from "./auth";
import { readMedia } from "./vault";

// Imagens só saem do cofre para quem está logado (checagem dupla: proxy + aqui).
// O acervo é servido por 16 rotas (m0…mf), uma por "fatia" do id, para que cada função
// carregue só 1/16 das imagens e fique dentro do limite de tamanho da Vercel.
export async function serveMedia(req: Request, params: Promise<{ id: string; size: string }>) {
  if (!(await currentUser())) return new NextResponse(null, { status: 401 });
  const { id, size } = await params;
  if (size !== "t" && size !== "f") return new NextResponse(null, { status: 404 });

  const etag = `"${id}.${size}"`;
  if (req.headers.get("if-none-match") === etag) return new NextResponse(null, { status: 304 });

  const data = await readMedia(id, size);
  if (!data) return new NextResponse(null, { status: 404 });
  const download = new URL(req.url).searchParams.get("dl");
  return new NextResponse(new Uint8Array(data), {
    headers: {
      "Content-Type": "image/webp",
      "Cache-Control": "private, max-age=2592000, immutable",
      ETag: etag,
      ...(download ? { "Content-Disposition": `attachment; filename="${download.replace(/[^\w.-]/g, "_")}.webp"` } : {}),
    },
  });
}
