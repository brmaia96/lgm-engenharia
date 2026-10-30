import { serveMedia } from "@/lib/media-route";

export async function GET(req: Request, ctx: RouteContext<"/api/m1/[id]/[size]">) {
  return serveMedia(req, ctx.params);
}
