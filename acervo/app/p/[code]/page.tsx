import type { Metadata } from "next";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { CopyButton } from "@/components/CopyButton";
import { Gallery } from "@/components/Gallery";
import { Mark } from "@/components/Logo";
import { RestoreButton } from "@/components/ProjectActions";
import { Topbar } from "@/components/Topbar";
import { currentUser } from "@/lib/auth";
import { CATEGORIAS, CATEGORIAS_ESSENCIAIS, PAVIMENTOS, TIPOS, terrenoLabel } from "@/lib/naming";
import { getAcervo, getProject, summarize } from "@/lib/vault";

export const dynamic = "force-dynamic";

export async function generateMetadata(props: PageProps<"/p/[code]">): Promise<Metadata> {
  const { code } = await props.params;
  return { title: code.toUpperCase() };
}

export default async function ProjectPage(props: PageProps<"/p/[code]">) {
  const user = await currentUser();
  if (!user) redirect("/login");
  const { code } = await props.params;
  const { salvo } = await props.searchParams;
  const p = await getProject(code);
  if (!p) notFound();

  const all = (await getAcervo()).projects;
  const idx = all.findIndex((x) => x.code === p.code);
  const prev = idx >= 0 && all.length > 1 ? all[(idx - 1 + all.length) % all.length] : null;
  const next = idx >= 0 && all.length > 1 ? all[(idx + 1) % all.length] : null;
  const cover = summarize(p).cover;
  const faltam = CATEGORIAS_ESSENCIAIS.filter((c) => !p.media.some((m) => m.cat === c));
  const fullName = `${p.code}_${p.name}`;
  const nd = <dd className="nd">a confirmar</dd>;

  const details: [string, React.ReactNode][] = [
    ["Tipo", TIPOS[p.tipo]],
    ["Dormitórios", p.quartos ?? "—"],
    ["Banheiros", p.banheiros ?? "—"],
    ["Vagas", p.vagas ?? "—"],
    ["Sistema", p.sistema ?? "—"],
    ["Estilo", p.estilo ?? "—"],
    ["Piscina", p.piscina ? "Sim" : "—"],
    ["Área gourmet", p.gourmet ? "Sim" : "—"],
    ["Data", p.data ?? "—"],
  ];

  return (
    <>
      <Topbar user={user} active="acervo" />
      {salvo && <div className="toast toast-auto" role="status">Alterações salvas</div>}
      <main>
        {p.lixeira && (
          <div className="trash-banner">
            <div className="wrap">
              <span>Este projeto está na lixeira{p.lixeira.motivo ? ` — ${p.lixeira.motivo}` : ""}.</span>
              <RestoreButton code={p.code} />
            </div>
          </div>
        )}
        <section className="p-hero">
          <Link href="/" className="p-back">← Acervo</Link>
          {cover ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={`/api/m/${cover}/f`} alt={p.titulo} />
          ) : (
            <div style={{ display: "grid", placeItems: "center", height: "100%", color: "#46403a" }}><Mark size={96} /></div>
          )}
          <div className="wrap reveal">
            <p className="eyebrow">{p.code} · {TIPOS[p.tipo]}</p>
            <h1>{p.titulo}</h1>
            <div className="codebar">
              <span>{p.name}</span>
              <CopyButton text={fullName} />
            </div>
          </div>
        </section>

        <dl className="specbar">
          <div className="wrap">
            <div><dt>Área construída</dt>{p.area != null ? <dd>{p.area.toLocaleString("pt-BR")}<small>m²</small></dd> : nd}</div>
            <div><dt>Terreno</dt>{p.terreno ? <dd>{terrenoLabel(p.terreno).toLowerCase()}<small>m</small></dd> : nd}</div>
            <div><dt>Suítes</dt>{p.suites != null ? <dd>{p.suites}</dd> : nd}</div>
            <div><dt>Pavimentos</dt><dd>{PAVIMENTOS[p.pavimentos]}</dd></div>
            <div><dt>Imagens</dt><dd>{p.media.length}</dd></div>
          </div>
        </dl>

        <div className="wrap p-body">
          <Gallery media={p.media} baseName={fullName} />
          <aside className="p-side">
            {p.descricao && <p className="desc">{p.descricao}</p>}
            <dl>
              {details.map(([k, v]) => (
                <div key={k}><dt>{k}</dt><dd>{v}</dd></div>
              ))}
            </dl>
            {p.tags?.length ? <div className="tags">{p.tags.map((t) => <span key={t}>{t}</span>)}</div> : null}
            {faltam.length > 0 && (
              <p className="pending">Ainda falta no acervo: {faltam.map((c) => CATEGORIAS[c].toLowerCase()).join(", ")}.</p>
            )}
            <div className="side-actions">
              <Link href={`/p/${p.code}/editar`} className="btn">Editar projeto</Link>
            </div>
            {p.editado && (
              <p className="side-note">
                Editado por <span style={{ textTransform: "capitalize" }}>{p.editado.por}</span> em{" "}
                {new Date(p.editado.em).toLocaleString("pt-BR", { timeZone: "America/Sao_Paulo", dateStyle: "short", timeStyle: "short" })}
              </p>
            )}
          </aside>
        </div>

        {prev && next && (
          <nav className="wrap pnav">
            <Link href={`/p/${prev.code}`}><small>← Anterior · {prev.code}</small><span>{prev.titulo}</span></Link>
            <Link href={`/p/${next.code}`}><small>{next.code} · Próximo →</small><span>{next.titulo}</span></Link>
          </nav>
        )}
      </main>
    </>
  );
}
