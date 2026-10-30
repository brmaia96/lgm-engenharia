import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { Mark } from "@/components/Logo";
import { Topbar } from "@/components/Topbar";
import { currentUser } from "@/lib/auth";
import { getLog } from "@/lib/vault";

export const metadata: Metadata = { title: "Histórico" };
export const dynamic = "force-dynamic";

const ACOES: Record<string, string> = { criou: "Criou", editou: "Editou", excluiu: "Excluiu", restaurou: "Restaurou" };

export default async function Historico(props: PageProps<"/historico">) {
  const user = await currentUser();
  if (!user) redirect("/login");
  const sp = await props.searchParams;
  const quem = typeof sp.quem === "string" ? sp.quem : "";
  const proj = typeof sp.p === "string" ? sp.p.toUpperCase() : "";
  const acao = typeof sp.acao === "string" ? sp.acao : "";
  const log = await getLog();
  const pessoas = [...new Set(log.map((r) => r.por))].sort();
  const lista = log.filter((r) => (!quem || r.por === quem) && (!proj || r.code === proj) && (!acao || r.acao === acao));
  const link = (k: string, v: string) => {
    const q = new URLSearchParams({ ...(quem ? { quem } : {}), ...(proj ? { p: proj } : {}), ...(acao ? { acao } : {}) });
    if (v) q.set(k, v); else q.delete(k);
    const s = q.toString();
    return `/historico${s ? `?${s}` : ""}`;
  };
  const fmt = (iso: string) => new Date(iso).toLocaleString("pt-BR", { timeZone: "America/Sao_Paulo", day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit" });

  return (
    <>
      <Topbar user={user} active="historico" />
      <main className="wrap">
        <div className="page-head">
          <div>
            <p className="eyebrow accent">Controle do acervo</p>
            <h1 className="display">Histórico</h1>
          </div>
          <div className="stats"><div><b>{log.length}</b><span>alterações</span></div></div>
        </div>

        <div className="hist-filters">
          <span className="eyebrow">Quem</span>
          <Link className="chip" aria-pressed={!quem} href={link("quem", "")}>Todos</Link>
          {pessoas.map((p) => <Link key={p} className="chip" aria-pressed={quem === p} href={link("quem", p)} style={{ textTransform: "capitalize" }}>{p}</Link>)}
          <span className="eyebrow" style={{ marginLeft: 12 }}>Ação</span>
          <Link className="chip" aria-pressed={!acao} href={link("acao", "")}>Todas</Link>
          {Object.entries(ACOES).map(([k, v]) => <Link key={k} className="chip" aria-pressed={acao === k} href={link("acao", k)}>{v}</Link>)}
          {proj && <Link className="pill" href={link("p", "")}><span>Projeto</span> {proj} ✕</Link>}
        </div>

        {lista.length === 0 ? (
          <div className="empty"><Mark size={40} /><p>Nenhuma alteração registrada{quem || proj || acao ? " com esses filtros" : " ainda"}.</p></div>
        ) : (
          <ol className="hist">
            {lista.map((r, i) => (
              <li key={i}>
                <div className="hist-when">
                  <span>{fmt(r.em)}</span>
                  <b style={{ textTransform: "capitalize" }}>{r.por}</b>
                </div>
                <div className="hist-what">
                  <p>
                    <span className={`hist-acao ${r.acao}`}>{ACOES[r.acao]}</span>{" "}
                    <Link href={`/p/${r.code}`} className="hist-proj">{r.code} · {r.titulo}</Link>
                    {" "}<Link href={link("p", r.code)} className="link">só este projeto</Link>
                  </p>
                  {r.mudancas.length > 0 && (
                    <ul>
                      {r.mudancas.map((m, j) => (
                        <li key={j}>
                          <span className="campo">{m.campo}</span>
                          {m.de !== undefined ? <><s>{m.de}</s> → <b>{m.para}</b></> : <b>{m.para}</b>}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              </li>
            ))}
          </ol>
        )}
      </main>
    </>
  );
}
