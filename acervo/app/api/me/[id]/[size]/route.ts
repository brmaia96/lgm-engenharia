import { serveMedia } from "@/lib/media-route";

export async function GET(req: Request, ctx: RouteContext<"/api/me/[id]/[size]">) {
  return serveMedia(req, ctx.params);
}
