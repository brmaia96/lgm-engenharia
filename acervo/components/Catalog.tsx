"use client";
import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import { CATEGORIAS_ESSENCIAIS, PAVIMENTOS, TIPOS, terrenoLabel } from "@/lib/naming";
import type { ProjetoResumo, Tipo } from "@/lib/types";
import { Mark } from "./Logo";

type Filters = Record<string, string[]>;
type Opt = { value: string; label: string };
type Group = { key: string; label: string; options: Opt[]; test: (p: ProjetoResumo, v: string) => boolean };

const PAGE = 24;
const FAV_KEY = "cb-favs";
const VIEW_KEY = "cb-view";

const inBand = (n: number | null | undefined, band: string) => {
  if (n == null) return false;
  const [a, b] = band.split("-");
  return n >= Number(a) && (b === "" || n < Number(b));
};
const norm = (s: string) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");

function useLocal<T>(key: string, initial: T) {
  const [v, setV] = useState<T>(initial);
  useEffect(() => {
    try {
      const raw = localStorage.getItem(key);
      if (raw) setV(JSON.parse(raw));
    } catch {}
  }, [key]);
  const set = (next: T) => {
    setV(next);
    try { localStorage.setItem(key, JSON.stringify(next)); } catch {}
  };
  return [v, set] as const;
}

export function Catalog({ projects, initial }: { projects: ProjetoResumo[]; initial: Record<string, string | string[] | undefined> }) {
  const groups = useMemo<Group[]>(() => {
    const uniq = (f: (p: ProjetoResumo) => string | undefined) =>
      [...new Set(projects.map(f).filter(Boolean) as string[])].sort((a, b) => a.localeCompare(b, "pt")).map((v) => ({ value: v, label: v }));
    const list: Group[] = [
      { key: "pav", label: "Pavimentos", options: Object.entries(PAVIMENTOS).map(([value, label]) => ({ value, label })), test: (p, v) => p.pavimentos === v },
      {
        key: "suites", label: "Suítes",
        options: [{ value: "0", label: "Sem suíte" }, { value: "1", label: "1 suíte" }, { value: "2", label: "2 suítes" }, { value: "3", label: "3 suítes" }, { value: "4", label: "4 ou mais" }],
        test: (p, v) => p.suites != null && (v === "4" ? p.suites >= 4 : p.suites === Number(v)),
      },
      {
        key: "area", label: "Área",
        options: [
          { value: "0-60", label: "Até 60 m²" }, { value: "60-100", label: "60 a 100 m²" }, { value: "100-150", label: "100 a 150 m²" },
          { value: "150-220", label: "150 a 220 m²" }, { value: "220-320", label: "220 a 320 m²" }, { value: "320-", label: "Acima de 320 m²" },
        ],
        test: (p, v) => inBand(p.area, v),
      },
      {
        key: "frente", label: "Terreno",
        options: [
          { value: "0-10", label: "Frente até 10 m" }, { value: "10-12", label: "Frente 10 a 12 m" }, { value: "12-15", label: "Frente 12 a 15 m" },
          { value: "15-20", label: "Frente 15 a 20 m" }, { value: "20-", label: "Frente acima de 20 m" }, { value: "nd", label: "A confirmar" },
        ],
        test: (p, v) => (v === "nd" ? !p.terreno : inBand(p.terreno?.frente, v)),
      },
      { key: "sistema", label: "Sistema", options: uniq((p) => p.sistema), test: (p, v) => p.sistema === v },
      { key: "estilo", label: "Estilo", options: uniq((p) => p.estilo), test: (p, v) => p.estilo === v },
      {
        key: "extra", label: "Características",
        options: [
          { value: "piscina", label: "Piscina" }, { value: "gourmet", label: "Área gourmet" },
          { value: "completo", label: "Fachada, interna, planta e layout" }, { value: "pendente", label: "Dados a confirmar" },
          { value: "rerender", label: "Precisa re-render" },
        ],
        test: (p, v) =>
          v === "piscina" ? Boolean(p.piscina)
          : v === "gourmet" ? Boolean(p.gourmet)
          : v === "pendente" ? p.area == null || p.suites == null || p.terreno == null || p.pavimentos === "ND"
          : v === "rerender" ? Boolean(p.tags?.includes("re-render"))
          : CATEGORIAS_ESSENCIAIS.every((c) => p.counts[c]),
      },
    ];
    return list.filter((g) => g.options.length > 0);
  }, [projects]);

  const pick = (k: string) => {
    const v = initial[k];
    return v ? (Array.isArray(v) ? v : v.split(",")).filter(Boolean) : [];
  };
  const [tipo, setTipo] = useState<string>(typeof initial.tipo === "string" ? initial.tipo : "");
  const [filters, setFilters] = useState<Filters>(() => Object.fromEntries(groups.map((g) => [g.key, pick(g.key)])));
  const [q, setQ] = useState(typeof initial.q === "string" ? initial.q : "");
  const [sort, setSort] = useState(typeof initial.ordem === "string" ? initial.ordem : "recentes");
  const [onlyFav, setOnlyFav] = useState(initial.fav === "1");
  const [favs, setFavs] = useLocal<string[]>(FAV_KEY, []);
  const [view, setView] = useLocal<"grade" | "lista">(VIEW_KEY, "grade");
  const [shown, setShown] = useState(PAGE);
  const [open, setOpen] = useState<string | null>(null);

  useEffect(() => {
    const sp = new URLSearchParams();
    if (tipo) sp.set("tipo", tipo);
    if (q) sp.set("q", q);
    for (const [k, v] of Object.entries(filters)) if (v.length) sp.set(k, v.join(","));
    if (sort !== "recentes") sp.set("ordem", sort);
    if (onlyFav) sp.set("fav", "1");
    const s = sp.toString();
    window.history.replaceState(null, "", s ? `?${s}` : window.location.pathname);
    setShown(PAGE);
  }, [tipo, filters, q, sort, onlyFav]);

  // fecha menus ao clicar fora / Esc
  useEffect(() => {
    if (!open) return;
    const close = (e: Event) => {
      if (e instanceof KeyboardEvent && e.key !== "Escape") return;
      if (e instanceof MouseEvent && (e.target as HTMLElement).closest(".dd")) return;
      setOpen(null);
    };
    document.addEventListener("mousedown", close);
    document.addEventListener("keydown", close);
    return () => { document.removeEventListener("mousedown", close); document.removeEventListener("keydown", close); };
  }, [open]);

  const matchQuery = (p: ProjetoResumo) => {
    const terms = norm(q).split(/\s+/).filter(Boolean);
    if (!terms.length) return true;
    const hay = norm([p.code, p.name, p.titulo, p.descricao, p.estilo, p.sistema, ...(p.tags ?? [])].join(" "));
    return terms.every((t) => hay.includes(t));
  };
  const passes = (p: ProjetoResumo, skip?: string) =>
    (skip === "tipo" || !tipo || p.tipo === tipo) &&
    matchQuery(p) &&
    (!onlyFav || favs.includes(p.code)) &&
    groups.every((g) => g.key === skip || !filters[g.key]?.length || filters[g.key].some((v) => g.test(p, v)));

  const results = useMemo(() => {
    const r = projects.filter((p) => passes(p));
    const by: Record<string, (a: ProjetoResumo, b: ProjetoResumo) => number> = {
      recentes: (a, b) => (b.data ?? "").localeCompare(a.data ?? "") || b.code.localeCompare(a.code),
      codigo: (a, b) => a.code.localeCompare(b.code),
      "area-asc": (a, b) => (a.area ?? 1e9) - (b.area ?? 1e9),
      "area-desc": (a, b) => (b.area ?? -1) - (a.area ?? -1),
      suites: (a, b) => (b.suites ?? -1) - (a.suites ?? -1) || (b.area ?? 0) - (a.area ?? 0),
    };
    return r.sort(by[sort] ?? by.recentes);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projects, tipo, filters, q, sort, onlyFav, favs]);

  // carrega mais ao chegar no fim
  const sentinel = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = sentinel.current;
    if (!el) return;
    const io = new IntersectionObserver((es) => es[0].isIntersecting && setShown((n) => n + PAGE), { rootMargin: "800px" });
    io.observe(el);
    return () => io.disconnect();
  }, [results.length, view]);

  const toggle = (key: string, value: string) =>
    setFilters((f) => {
      const cur = f[key] ?? [];
      return { ...f, [key]: cur.includes(value) ? cur.filter((v) => v !== value) : [...cur, value] };
    });
  const activeCount = Object.values(filters).reduce((n, v) => n + v.length, 0) + (onlyFav ? 1 : 0) + (q ? 1 : 0);
  const clearAll = () => { setFilters({}); setQ(""); setOnlyFav(false); };
  const toggleFav = (code: string) => setFavs(favs.includes(code) ? favs.filter((c) => c !== code) : [...favs, code]);

  const tipos = (Object.keys(TIPOS) as Tipo[]).filter((t) => projects.some((p) => p.tipo === t));
  const countTipo = (t: string) => projects.filter((p) => passes({ ...p }, "tipo") && (!t || p.tipo === t)).length;
  const main = groups.filter((g) => ["pav", "suites", "area", "frente"].includes(g.key));
  const extra = groups.filter((g) => !["pav", "suites", "area", "frente"].includes(g.key));
  const label = (g: Group, v: string) => g.options.find((o) => o.value === v)?.label ?? v;
  const sorts: Opt[] = [
    { value: "recentes", label: "Mais recentes" }, { value: "codigo", label: "Código" },
    { value: "area-asc", label: "Menor área" }, { value: "area-desc", label: "Maior área" }, { value: "suites", label: "Mais suítes" },
  ];

  const Options = ({ g }: { g: Group }) => (
    <>
      {g.options.map((o) => {
        const on = filters[g.key]?.includes(o.value) ?? false;
        const n = projects.filter((p) => passes(p, g.key) && g.test(p, o.value)).length;
        return (
          <button key={o.value} className="opt" role="menuitemcheckbox" aria-checked={on} disabled={!n && !on} onClick={() => toggle(g.key, o.value)}>
            <span className="box" />{o.label}<small>{n}</small>
          </button>
        );
      })}
    </>
  );

  return (
    <>
      <div className="wrap">
        <div className="collections" role="tablist" aria-label="Coleções">
          <button role="tab" aria-selected={!tipo} onClick={() => setTipo("")}>Todos<sup>{countTipo("")}</sup></button>
          {tipos.map((t) => (
            <button key={t} role="tab" aria-selected={tipo === t} onClick={() => setTipo(t)}>{TIPOS[t]}<sup>{countTipo(t)}</sup></button>
          ))}
        </div>
      </div>

      <div className="filterbar">
        <div className="wrap">
          <label className="search">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"><circle cx="11" cy="11" r="7" /><path d="m20 20-3.5-3.5" /></svg>
            <input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Buscar por código, nome ou característica" aria-label="Buscar" />
          </label>
          <span className="fb-sep" />
          {main.map((g) => (
            <div className="dd" key={g.key}>
              <button aria-expanded={open === g.key} onClick={() => setOpen(open === g.key ? null : g.key)}>
                {g.label}{filters[g.key]?.length ? <span className="n">{filters[g.key].length}</span> : <Caret />}
              </button>
              {open === g.key && <div className="dd-pop" role="menu"><Options g={g} /></div>}
            </div>
          ))}
          <div className="dd">
            <button aria-expanded={open === "mais"} onClick={() => setOpen(open === "mais" ? null : "mais")}>
              Mais filtros{extra.reduce((n, g) => n + (filters[g.key]?.length ?? 0), 0) ? <span className="n">{extra.reduce((n, g) => n + (filters[g.key]?.length ?? 0), 0)}</span> : <Caret />}
            </button>
            {open === "mais" && (
              <div className="dd-pop" role="menu" style={{ minWidth: 300 }}>
                {extra.map((g) => (<div key={g.key}><h4>{g.label}</h4><Options g={g} /></div>))}
              </div>
            )}
          </div>
          <button className="chip" aria-pressed={onlyFav} onClick={() => setOnlyFav(!onlyFav)}>
            <svg width="12" height="12" viewBox="0 0 24 24" fill={onlyFav ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2"><path d="m12 3 2.8 5.8 6.2.9-4.5 4.4 1 6.2L12 17.4l-5.5 2.9 1-6.2L3 9.7l6.2-.9Z" /></svg>
            Favoritos {favs.length > 0 && <small>{favs.length}</small>}
          </button>
          <div className="fb-right">
            <span className="count">{results.length} {results.length === 1 ? "projeto" : "projetos"}</span>
            <div className="dd">
              <button aria-expanded={open === "ordem"} onClick={() => setOpen(open === "ordem" ? null : "ordem")}>
                {sorts.find((s) => s.value === sort)?.label}<Caret />
              </button>
              {open === "ordem" && (
                <div className="dd-pop right" role="menu">
                  {sorts.map((s) => (
                    <button key={s.value} className="opt" role="menuitemradio" aria-checked={sort === s.value} onClick={() => { setSort(s.value); setOpen(null); }}>
                      <span className="box" />{s.label}
                    </button>
                  ))}
                </div>
              )}
            </div>
            <div className="view-toggle" role="group" aria-label="Visualização">
              <button aria-pressed={view === "grade"} onClick={() => setView("grade")} aria-label="Grade" title="Grade">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"><rect x="3" y="3" width="7" height="7" /><rect x="14" y="3" width="7" height="7" /><rect x="3" y="14" width="7" height="7" /><rect x="14" y="14" width="7" height="7" /></svg>
              </button>
              <button aria-pressed={view === "lista"} onClick={() => setView("lista")} aria-label="Lista" title="Lista">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"><path d="M3 6h18M3 12h18M3 18h18" /></svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <section className="wrap results">
        {activeCount > 0 && (
          <div className="active-pills" style={{ paddingTop: 0, paddingBottom: 28 }}>
            {q && <button className="pill" onClick={() => setQ("")}><span>Busca</span> “{q}” ✕</button>}
            {onlyFav && <button className="pill" onClick={() => setOnlyFav(false)}>Favoritos ✕</button>}
            {groups.flatMap((g) => (filters[g.key] ?? []).map((v) => (
              <button key={g.key + v} className="pill" onClick={() => toggle(g.key, v)}><span>{g.label}</span> {label(g, v)} ✕</button>
            )))}
            <button className="link" onClick={clearAll}>Limpar tudo</button>
          </div>
        )}

        {results.length === 0 ? (
          <div className="empty">
            <Mark size={40} />
            <p>{projects.length ? "Nenhum projeto com esses filtros." : "O acervo ainda está vazio."}</p>
            {activeCount > 0 && <button className="btn" onClick={clearAll}>Limpar filtros</button>}
          </div>
        ) : view === "grade" ? (
          <div className="grid">
            {results.slice(0, shown).map((p, i) => (
              <Card key={p.code} p={p} fav={favs.includes(p.code)} onFav={() => toggleFav(p.code)} eager={i < 6} />
            ))}
          </div>
        ) : (
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th />
                  <th onClick={() => setSort("codigo")}>Código</th>
                  <th>Projeto</th>
                  <th className="num" onClick={() => setSort(sort === "area-desc" ? "area-asc" : "area-desc")}>Área</th>
                  <th className="num" onClick={() => setSort("suites")}>Suítes</th>
                  <th className="hide-sm">Terreno</th>
                  <th className="hide-sm">Pavimentos</th>
                  <th className="hide-sm num">Imagens</th>
                </tr>
              </thead>
              <tbody>
                {results.slice(0, shown).map((p) => (
                  <tr key={p.code}>
                    <td>
                      <Link href={`/p/${p.code}`}>
                        {p.cover ? (
                          // eslint-disable-next-line @next/next/no-img-element
                          <img className="thumb" src={`/api/m/${p.cover}/t`} alt="" loading="lazy" />
                        ) : <span className="thumb" />}
                      </Link>
                    </td>
                    <td className="mono">{p.code}</td>
                    <td><Link href={`/p/${p.code}`} className="t-title">{p.titulo}</Link><div className="card-name">{p.name}</div></td>
                    <td className="num">{p.area != null ? `${p.area.toLocaleString("pt-BR")} m²` : "—"}</td>
                    <td className="num">{p.suites ?? "—"}</td>
                    <td className="hide-sm">{p.terreno ? terrenoLabel(p.terreno).toLowerCase() : "—"}</td>
                    <td className="hide-sm">{PAVIMENTOS[p.pavimentos]}</td>
                    <td className="hide-sm num">{Object.values(p.counts).reduce((a, b) => a + (b ?? 0), 0)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {shown < results.length && (
          <div className="more" ref={sentinel}>
            <button className="btn" onClick={() => setShown((n) => n + PAGE)}>Ver mais ({results.length - shown})</button>
          </div>
        )}
      </section>
    </>
  );
}

function Caret() {
  return <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="m6 9 6 6 6-6" /></svg>;
}

function Card({ p, fav, onFav, eager }: { p: ProjetoResumo; fav: boolean; onFav: () => void; eager: boolean }) {
  const total = Object.values(p.counts).reduce((a, b) => a + (b ?? 0), 0);
  return (
    <article className="card">
      <Link href={`/p/${p.code}`} className="card-media">
        {p.cover ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={`/api/m/${p.cover}/t`} alt={p.titulo} loading={eager ? "eager" : "lazy"} decoding="async" />
        ) : (
          <span className="ph"><Mark size={48} /></span>
        )}
        <span className="card-count">{total} {total === 1 ? "imagem" : "imagens"}</span>
      </Link>
      <button className="card-fav" aria-pressed={fav} onClick={onFav} aria-label={fav ? "Remover dos favoritos" : "Favoritar"}>
        <svg width="15" height="15" viewBox="0 0 24 24" fill={fav ? "currentColor" : "none"} stroke="currentColor" strokeWidth="1.6"><path d="m12 3 2.8 5.8 6.2.9-4.5 4.4 1 6.2L12 17.4l-5.5 2.9 1-6.2L3 9.7l6.2-.9Z" /></svg>
      </button>
      <Link href={`/p/${p.code}`} className="card-body">
        <div className="card-meta">
          <span className="eyebrow">{p.code} · {TIPOS[p.tipo]}</span>
          <span className="eyebrow">{PAVIMENTOS[p.pavimentos]}</span>
        </div>
        <h3 className="card-title">{p.titulo}</h3>
        <span className="card-name">{p.name}</span>
        <div className="ficha">
          <span>Área<strong className={p.area == null ? "nd" : ""}>{p.area != null ? `${p.area.toLocaleString("pt-BR")} m²` : "a confirmar"}</strong></span>
          <span>Suítes<strong className={p.suites == null ? "nd" : ""}>{p.suites ?? "—"}</strong></span>
          <span>Terreno<strong className={!p.terreno ? "nd" : ""}>{p.terreno ? terrenoLabel(p.terreno).toLowerCase() : "—"}</strong></span>
        </div>
      </Link>
    </article>
  );
}
