import type { Metadata } from "next";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { CopyButton } from "@/components/CopyButton";
import { Gallery } from "@/components/Gallery";
import { Mark } from "@/components/Logo";
import { Topbar } from "@/components/Topbar";
import { currentUser } from "@/lib/auth";
import { CATEGORIAS, CATEGORIAS_ESSENCIAIS, PAVIMENTOS, TIPOS, terrenoLabel } from "@/lib/naming";
import { getCatalog, getProject } from "@/lib/vault";

export const dynamic = "force-dynamic";

export async function generateMetadata(props: PageProps<"/p/[code]">): Promise<Metadata> {
  const { code } = await props.params;
  return { title: code.toUpperCase() };
}

export default async function ProjectPage(props: PageProps<"/p/[code]">) {
  const user = await currentUser();
  if (!user) redirect("/login");
  const { code } = await props.params;
  const p = await getProject(code);
  if (!p) notFound();

  const all = (await getCatalog()).projects;
  const idx = all.findIndex((x) => x.code === p.code);
  const prev = all[(idx - 1 + all.length) % all.length];
  const next = all[(idx + 1) % all.length];
  const cover = p.cover ?? p.media.find((m) => m.cat === "fachada")?.id ?? p.media[0]?.id;
  const faltam = CATEGORIAS_ESSENCIAIS.filter((c) => !p.media.some((m) => m.cat === c));
  const fullName = `${p.code}_${p.name}`;

  const specs: [string, React.ReactNode][] = [
    ["Área construída", p.area != null ? <>{p.area}<small> m²</small></> : <small>a confirmar</small>],
    ["Terreno", p.terreno ? <>{terrenoLabel(p.terreno).toLowerCase()}<small> m · {Math.round(p.terreno.frente * p.terreno.fundo)} m²</small></> : <small>a confirmar</small>],
    ["Suítes", p.suites ?? <small>a confirmar</small>],
    ["Dormitórios", p.quartos ?? "—"],
    ["Banheiros", p.banheiros ?? "—"],
    ["Vagas", p.vagas ?? "—"],
    ["Pavimentos", PAVIMENTOS[p.pavimentos]],
    ["Tipo", TIPOS[p.tipo]],
    ["Sistema", p.sistema ?? "—"],
    ["Estilo", p.estilo ?? "—"],
  ];

  return (
    <>
      <Topbar user={user} active="acervo" />
      <main>
        <section className="p-hero">
          <Link href="/" className="p-back">← Acervo</Link>
          {cover ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={`/api/m/${cover}/f`} alt={p.titulo} />
          ) : (
            <div style={{ display: "grid", placeItems: "center", height: "100%" }}><Mark size={96} /></div>
          )}
          <div className="wrap">
            <p className="eyebrow">{TIPOS[p.tipo]}{p.area != null ? ` · ${p.area} m²` : ""}{p.suites != null ? ` · ${p.suites} ${p.suites === 1 ? "suíte" : "suítes"}` : ""}</p>
            <h1 className="display">{p.titulo}</h1>
            <div className="codebar mono">
              <b>{p.code}</b> <span>{p.name}</span>
              <CopyButton text={fullName} />
            </div>
          </div>
        </section>

        <div className="wrap p-body">
          <Gallery media={p.media} baseName={fullName} />
          <aside className="p-side">
            <div className="sheet">
              <div className="sheet-head">
                <Mark size={22} />
                <div>
                  <div className="mono" style={{ fontWeight: 600 }}>{p.code}</div>
                  <div className="eyebrow" style={{ letterSpacing: ".12em" }}>Ficha técnica</div>
                </div>
              </div>
              <dl>
                {specs.map(([k, v]) => (
                  <div key={k}><dt>{k}</dt><dd>{v}</dd></div>
                ))}
              </dl>
              {(p.piscina || p.gourmet) && (
                <div className="tags" style={{ paddingTop: 16 }}>
                  {p.piscina && <span>Piscina</span>}
                  {p.gourmet && <span>Área gourmet</span>}
                </div>
              )}
              {p.descricao && <p className="desc">{p.descricao}</p>}
              {p.tags?.length ? <div className="tags">{p.tags.map((t) => <span key={t}>{t}</span>)}</div> : null}
              {faltam.length > 0 && (
                <p className="desc" style={{ borderTop: "1px solid var(--linha)", fontSize: 12 }}>
                  Pendente no acervo: {faltam.map((c) => CATEGORIAS[c].toLowerCase()).join(", ")}.
                </p>
              )}
            </div>
          </aside>
        </div>

        {all.length > 1 && (
          <nav className="wrap pnav">
            <Link href={`/p/${prev.code}`}><small>← Anterior</small><span className="mono">{prev.code}</span>{prev.titulo}</Link>
            <Link href={`/p/${next.code}`}><small>Próximo →</small><span className="mono">{next.code}</span>{next.titulo}</Link>
          </nav>
        )}
      </main>
    </>
  );
}
