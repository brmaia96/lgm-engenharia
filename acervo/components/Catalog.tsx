"use client";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { CATEGORIAS_ESSENCIAIS, PAVIMENTOS, TIPOS, terrenoLabel } from "@/lib/naming";
import type { ProjetoResumo } from "@/lib/types";
import { Mark } from "./Logo";

type Filters = Record<string, string[]>;
type Group = {
  key: string;
  label: string;
  options: { value: string; label: string }[];
  test: (p: ProjetoResumo, value: string) => boolean;
};

const inBand = (n: number | undefined, band: string) => {
  if (n == null) return false;
  const [a, b] = band.split("-");
  return n >= Number(a) && (b === "" || n < Number(b));
};

const FAV_KEY = "cb-favs";

function useFavs() {
  const [favs, setFavs] = useState<string[]>([]);
  useEffect(() => {
    try { setFavs(JSON.parse(localStorage.getItem(FAV_KEY) ?? "[]")); } catch {}
  }, []);
  const toggle = (code: string) =>
    setFavs((f) => {
      const n = f.includes(code) ? f.filter((c) => c !== code) : [...f, code];
      try { localStorage.setItem(FAV_KEY, JSON.stringify(n)); } catch {}
      return n;
    });
  return { favs, toggle };
}

export function Catalog({ projects, initial }: { projects: ProjetoResumo[]; initial: Record<string, string | string[] | undefined> }) {
  const groups = useMemo<Group[]>(() => {
    const uniq = (f: (p: ProjetoResumo) => string | undefined) =>
      [...new Set(projects.map(f).filter(Boolean) as string[])].sort((a, b) => a.localeCompare(b, "pt"));
    const list: Group[] = [
      { key: "tipo", label: "Tipo", options: Object.entries(TIPOS).map(([value, label]) => ({ value, label })), test: (p, v) => p.tipo === v },
      { key: "pav", label: "Pavimentos", options: Object.entries(PAVIMENTOS).map(([value, label]) => ({ value, label })), test: (p, v) => p.pavimentos === v },
      {
        key: "suites", label: "Suítes",
        options: [{ value: "0", label: "Sem suíte" }, { value: "1", label: "1" }, { value: "2", label: "2" }, { value: "3", label: "3" }, { value: "4", label: "4+" }],
        test: (p, v) => p.suites != null && (v === "4" ? p.suites >= 4 : p.suites === Number(v)),
      },
      {
        key: "area", label: "Área construída",
        options: [
          { value: "0-60", label: "até 60 m²" }, { value: "60-100", label: "60–100" }, { value: "100-150", label: "100–150" },
          { value: "150-220", label: "150–220" }, { value: "220-320", label: "220–320" }, { value: "320-", label: "320+" },
        ],
        test: (p, v) => inBand(p.area ?? undefined, v),
      },
      {
        key: "frente", label: "Frente do terreno",
        options: [
          { value: "0-10", label: "até 10 m" }, { value: "10-12", label: "10–12" }, { value: "12-15", label: "12–15" },
          { value: "15-20", label: "15–20" }, { value: "20-", label: "20+" }, { value: "livre", label: "A confirmar" },
        ],
        test: (p, v) => (v === "livre" ? !p.terreno : inBand(p.terreno?.frente, v)),
      },
      { key: "sistema", label: "Sistema construtivo", options: uniq((p) => p.sistema).map((v) => ({ value: v, label: v })), test: (p, v) => p.sistema === v },
      { key: "estilo", label: "Estilo", options: uniq((p) => p.estilo).map((v) => ({ value: v, label: v })), test: (p, v) => p.estilo === v },
      {
        key: "extra", label: "Extras",
        options: [
          { value: "piscina", label: "Piscina" }, { value: "gourmet", label: "Área gourmet" },
          { value: "completo", label: "Com as 4 categorias" }, { value: "interna", label: "Tem internas" },
          { value: "pendente", label: "Dados a confirmar" }, { value: "rerender", label: "Precisa re-render" },
        ],
        test: (p, v) =>
          v === "piscina" ? Boolean(p.piscina)
          : v === "gourmet" ? Boolean(p.gourmet)
          : v === "interna" ? Boolean(p.counts.interna)
          : v === "pendente" ? p.area == null || p.suites == null || p.terreno == null
          : v === "rerender" ? Boolean(p.tags?.includes("re-render"))
          : CATEGORIAS_ESSENCIAIS.every((c) => p.counts[c]),
      },
    ];
    return list.filter((g) => g.options.length > 0);
  }, [projects]);

  const [filters, setFilters] = useState<Filters>(() => {
    const f: Filters = {};
    for (const g of groups) {
      const v = initial[g.key];
      if (v) f[g.key] = (Array.isArray(v) ? v : v.split(",")).filter(Boolean);
    }
    return f;
  });
  const [q, setQ] = useState(typeof initial.q === "string" ? initial.q : "");
  const [sort, setSort] = useState(typeof initial.ordem === "string" ? initial.ordem : "recentes");
  const [onlyFav, setOnlyFav] = useState(initial.fav === "1");
  const [drawer, setDrawer] = useState(false);
  const { favs, toggle } = useFavs();

  // filtros na URL: dá pra mandar o link filtrado um pro outro
  useEffect(() => {
    const sp = new URLSearchParams();
    if (q) sp.set("q", q);
    for (const [k, v] of Object.entries(filters)) if (v.length) sp.set(k, v.join(","));
    if (sort !== "recentes") sp.set("ordem", sort);
    if (onlyFav) sp.set("fav", "1");
    const s = sp.toString();
    window.history.replaceState(null, "", s ? `?${s}` : window.location.pathname);
  }, [filters, q, sort, onlyFav]);

  const matchQuery = (p: ProjetoResumo) => {
    if (!q.trim()) return true;
    const hay = [p.code, p.name, p.titulo, p.descricao, p.estilo, p.sistema, ...(p.tags ?? [])].join(" ").toLowerCase()
      .normalize("NFD").replace(/[̀-ͯ]/g, "");
    return q.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").split(/\s+/).every((t) => hay.includes(t));
  };
  const passes = (p: ProjetoResumo, skip?: string) =>
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
  }, [projects, filters, q, sort, onlyFav, favs]);

  const toggleFilter = (key: string, value: string) =>
    setFilters((f) => {
      const cur = f[key] ?? [];
      return { ...f, [key]: cur.includes(value) ? cur.filter((v) => v !== value) : [...cur, value] };
    });
  const active = Object.values(filters).reduce((n, v) => n + v.length, 0) + (onlyFav ? 1 : 0);
  const clearAll = () => { setFilters({}); setQ(""); setOnlyFav(false); };

  return (
    <>
      <div className="toolbar">
        <div className="wrap">
          <label className="search">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="7" /><path d="m20 20-3.5-3.5" /></svg>
            <input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Buscar código, nome, estilo… ex.: CB012, 3SUITES, piscina" aria-label="Buscar" />
          </label>
          <button className="btn filter-toggle" onClick={() => setDrawer(true)}>Filtros{active ? ` (${active})` : ""}</button>
          <select value={sort} onChange={(e) => setSort(e.target.value)} aria-label="Ordenar">
            <option value="recentes">Mais recentes</option>
            <option value="codigo">Código</option>
            <option value="area-asc">Menor área</option>
            <option value="area-desc">Maior área</option>
            <option value="suites">Mais suítes</option>
          </select>
          <span className="count">{results.length} de {projects.length}</span>
        </div>
      </div>

      <div className="wrap layout">
        <aside className={`filters${drawer ? " open" : ""}`} aria-label="Filtros">
          <div className="filters-head">
            <b>Filtros · {results.length} projetos</b>
            <button className="btn" onClick={() => setDrawer(false)}>Ver resultados</button>
          </div>
          <div className="fgroup">
            <h3>Seleção {active > 0 && <button onClick={clearAll}>limpar tudo</button>}</h3>
            <div className="chips">
              <button className="chip" aria-pressed={onlyFav} onClick={() => setOnlyFav((v) => !v)}>★ Favoritos <small>{favs.length}</small></button>
            </div>
          </div>
          {groups.map((g) => (
            <div className="fgroup" key={g.key}>
              <h3>{g.label}{filters[g.key]?.length ? <button onClick={() => setFilters((f) => ({ ...f, [g.key]: [] }))}>limpar</button> : null}</h3>
              <div className="chips">
                {g.options.map((o) => {
                  const on = filters[g.key]?.includes(o.value) ?? false;
                  const n = projects.filter((p) => passes(p, g.key) && g.test(p, o.value)).length;
                  if (!n && !on) return null;
                  return (
                    <button key={o.value} className="chip" aria-pressed={on} onClick={() => toggleFilter(g.key, o.value)}>
                      {o.label} <small>{n}</small>
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </aside>

        <section>
          {results.length === 0 ? (
            <div className="empty">
              <Mark size={48} />
              <p>{projects.length ? "Nenhum projeto com esses filtros." : "O acervo ainda está vazio. Veja a aba Padrão para incluir projetos."}</p>
              {active > 0 && <button className="btn" onClick={clearAll}>Limpar filtros</button>}
            </div>
          ) : (
            <div className="grid">
              {results.map((p, i) => <Card key={p.code} p={p} fav={favs.includes(p.code)} onFav={() => toggle(p.code)} eager={i < 6} />)}
            </div>
          )}
        </section>
      </div>
    </>
  );
}

function Card({ p, fav, onFav, eager }: { p: ProjetoResumo; fav: boolean; onFav: () => void; eager: boolean }) {
  return (
    <article className="card">
      <Link href={`/p/${p.code}`} className="card-media">
        {p.cover ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={`/api/m/${p.cover}/t`} alt={p.titulo} loading={eager ? "eager" : "lazy"} decoding="async" />
        ) : (
          <span className="ph"><Mark size={56} /></span>
        )}
        <span className="card-code mono">{p.code}</span>
        <span className="card-dots">
          {CATEGORIAS_ESSENCIAIS.map((c) => (
            <span key={c} className={p.counts[c] ? "" : "off"} title={c}>{{ fachada: "FAC", interna: "INT", planta: "PB", layout: "LAY" }[c as string]}</span>
          ))}
        </span>
      </Link>
      <button className="card-fav" aria-pressed={fav} onClick={onFav} aria-label={fav ? "Remover dos favoritos" : "Favoritar"}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill={fav ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2"><path d="m12 3 2.8 5.8 6.2.9-4.5 4.4 1 6.2L12 17.4l-5.5 2.9 1-6.2L3 9.7l6.2-.9Z" /></svg>
      </button>
      <Link href={`/p/${p.code}`} style={{ display: "grid", gap: 6 }}>
        <span className="card-title">{p.titulo}</span>
        <span className="card-name mono">{p.name}</span>
        <span className="specs">
          <span><b>{p.area ?? "—"}</b> m²</span>
          <span><b>{p.suites ?? "—"}</b> {p.suites === 1 ? "suíte" : "suítes"}</span>
          <span>terreno <b>{terrenoLabel(p.terreno).toLowerCase()}</b></span>
          <span>{PAVIMENTOS[p.pavimentos]}</span>
        </span>
      </Link>
    </article>
  );
}
