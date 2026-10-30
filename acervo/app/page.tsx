import { Catalog } from "@/components/Catalog";
import { Topbar } from "@/components/Topbar";
import { currentUser } from "@/lib/auth";
import { getAcervo, summarize } from "@/lib/vault";
import { redirect } from "next/navigation";

export const dynamic = "force-dynamic";

export default async function Home(props: PageProps<"/">) {
  const user = await currentUser();
  if (!user) redirect("/login");
  const catalog = await getAcervo();
  const projects = catalog.projects.map(summarize);
  const imgs = catalog.projects.reduce((n, p) => n + p.media.length, 0);
  const m2 = catalog.projects.reduce((n, p) => n + (p.area ?? 0), 0);

  return (
    <>
      <Topbar user={user} active="acervo" />
      <main>
        <div className="wrap page-head reveal">
          <div>
            <p className="eyebrow accent">Acervo de arquitetura</p>
            <h1 className="display">Projetos</h1>
          </div>
          <a href="/novo" className="btn primary">+ Novo projeto</a>
          <div className="stats">
            <div><b>{projects.length}</b><span>projetos</span></div>
            <div><b>{imgs.toLocaleString("pt-BR")}</b><span>imagens</span></div>
            <div><b>{Math.round(m2).toLocaleString("pt-BR")}</b><span>m² projetados</span></div>
          </div>
        </div>
        <Catalog projects={projects} initial={await props.searchParams} />
      </main>
    </>
  );
}
