import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { Mark } from "@/components/Logo";
import { RestoreButton } from "@/components/ProjectActions";
import { Topbar } from "@/components/Topbar";
import { currentUser } from "@/lib/auth";
import { getAcervo, summarize } from "@/lib/vault";

export const metadata: Metadata = { title: "Lixeira" };
export const dynamic = "force-dynamic";

export default async function Lixeira() {
  const user = await currentUser();
  if (!user) redirect("/login");
  const { trash } = await getAcervo();
  const items = trash.map((p) => ({ ...summarize(p), lixeira: p.lixeira! })).sort((a, b) => b.lixeira.em.localeCompare(a.lixeira.em));
  return (
    <>
      <Topbar user={user} active="lixeira" />
      <main className="wrap">
        <div className="page-head">
          <div>
            <p className="eyebrow accent">Fora do acervo · pode restaurar</p>
            <h1 className="display">Lixeira</h1>
          </div>
          <div className="stats"><div><b>{items.length}</b><span>projetos</span></div></div>
        </div>
        {items.length === 0 ? (
          <div className="empty"><Mark size={48} /><p>Nada na lixeira.</p></div>
        ) : (
          <div className="trash-list">
            {items.map((p) => (
              <div className="trash-row" key={p.code}>
                <Link href={`/p/${p.code}`} className="trash-thumb">
                  {p.cover ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img src={`/api/m/${p.cover}/t`} alt="" loading="lazy" />
                  ) : <Mark size={32} />}
                </Link>
                <div className="trash-info">
                  <span className="eyebrow">{p.code}</span>
                  <Link href={`/p/${p.code}`} className="t">{p.titulo}</Link>
                  <span className="m">
                    {p.lixeira.motivo ? `${p.lixeira.motivo} · ` : ""}por {p.lixeira.por} em {new Date(p.lixeira.em).toLocaleDateString("pt-BR", { timeZone: "America/Sao_Paulo" })}
                  </span>
                </div>
                <RestoreButton code={p.code} compact />
              </div>
            ))}
          </div>
        )}
      </main>
    </>
  );
}
