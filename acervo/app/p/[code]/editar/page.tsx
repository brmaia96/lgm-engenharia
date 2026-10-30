import type { Metadata } from "next";
import { notFound, redirect } from "next/navigation";
import { ProjectEditor } from "@/components/ProjectEditor";
import { Topbar } from "@/components/Topbar";
import { currentUser } from "@/lib/auth";
import { storeMode } from "@/lib/store";
import { getAcervo, getBaseProject, getProject } from "@/lib/vault";

export const dynamic = "force-dynamic";

export async function generateMetadata(props: PageProps<"/p/[code]/editar">): Promise<Metadata> {
  const { code } = await props.params;
  return { title: `Editar ${code.toUpperCase()}` };
}

export default async function EditPage(props: PageProps<"/p/[code]/editar">) {
  const user = await currentUser();
  if (!user) redirect("/login");
  const { code } = await props.params;
  const [p, base, { rev }] = await Promise.all([getProject(code), getBaseProject(code), getAcervo()]);
  if (!p) notFound();
  const all = [...p.media, ...(p.retiradas ?? []), ...(base?.media ?? [])];
  const baseMedia = all.filter((m, i) => all.findIndex((x) => x.id === m.id) === i);
  return (
    <>
      <Topbar user={user} active="acervo" />
      {storeMode() === "readonly" ? (
        <main className="wrap doc"><p>A edição pelo site ainda não está ativada neste servidor (falta o armazenamento de edições).</p></main>
      ) : (
        <ProjectEditor project={p} baseMedia={baseMedia} rev={rev} />
      )}
    </>
  );
}
