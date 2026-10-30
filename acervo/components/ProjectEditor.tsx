"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { buildName, CATEGORIAS, PAVIMENTOS, TIPOS } from "@/lib/naming";
import type { Categoria, Midia, Pavimento, Projeto, Tipo } from "@/lib/types";
import { call, DeleteButton } from "./ProjectActions";

type Item = { id: string; cat: Categoria; legenda: string; w: number; h: number };

const numStr = (n: number | null | undefined) => (n == null ? "" : String(n));
const toNum = (s: string) => (s.trim() === "" ? null : Number(s.replace(",", ".")));

export function ProjectEditor({ project, baseMedia, rev }: { project: Projeto; baseMedia: Midia[]; rev: number }) {
  const router = useRouter();
  const p = project;
  const [f, setF] = useState({
    titulo: p.titulo,
    descricao: p.descricao ?? "",
    tipo: p.tipo,
    pavimentos: p.pavimentos,
    frente: numStr(p.terreno?.frente),
    fundo: numStr(p.terreno?.fundo),
    area: numStr(p.area),
    suites: numStr(p.suites),
    quartos: numStr(p.quartos),
    banheiros: numStr(p.banheiros),
    vagas: numStr(p.vagas),
    piscina: Boolean(p.piscina),
    gourmet: Boolean(p.gourmet),
    destaque: Boolean(p.destaque),
    sistema: p.sistema ?? "",
    estilo: p.estilo ?? "",
    data: p.data ?? "",
    tags: (p.tags ?? []).join(", "),
  });
  const [items, setItems] = useState<Item[]>(p.media.map((m) => ({ id: m.id, cat: m.cat, legenda: m.legenda ?? "", w: m.w, h: m.h })));
  const [cover, setCover] = useState(p.cover ?? p.media.find((m) => m.cat === "fachada")?.id ?? p.media[0]?.id ?? "");
  const [dirty, setDirty] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const removed = baseMedia.filter((m) => !items.some((i) => i.id === m.id));
  const set = <K extends keyof typeof f>(k: K, v: (typeof f)[K]) => {
    setF((s) => ({ ...s, [k]: v }));
    setDirty(true);
  };
  const setItem = (id: string, patch: Partial<Item>) => {
    setItems((list) => list.map((i) => (i.id === id ? { ...i, ...patch } : i)));
    setDirty(true);
  };
  const move = (idx: number, d: number) => {
    setItems((list) => {
      const n = [...list];
      const j = idx + d;
      if (j < 0 || j >= n.length) return list;
      [n[idx], n[j]] = [n[j], n[idx]];
      return n;
    });
    setDirty(true);
  };

  useEffect(() => {
    const warn = (e: BeforeUnloadEvent) => {
      if (dirty) e.preventDefault();
    };
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [dirty]);

  const terreno = toNum(f.frente) && toNum(f.fundo) ? { frente: toNum(f.frente)!, fundo: toNum(f.fundo)! } : null;
  const preview = useMemo(
    () => buildName({ tipo: f.tipo, pavimentos: f.pavimentos, terreno, area: toNum(f.area), suites: toNum(f.suites) }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [f.tipo, f.pavimentos, f.frente, f.fundo, f.area, f.suites],
  );

  async function save() {
    setBusy(true);
    setError("");
    try {
      await call(`/api/projetos/${p.code}`, "PATCH", {
        rev,
        titulo: f.titulo,
        descricao: f.descricao,
        tipo: f.tipo,
        pavimentos: f.pavimentos,
        terreno,
        area: toNum(f.area),
        suites: toNum(f.suites),
        quartos: toNum(f.quartos),
        banheiros: toNum(f.banheiros),
        vagas: toNum(f.vagas),
        piscina: f.piscina,
        gourmet: f.gourmet,
        destaque: f.destaque,
        sistema: f.sistema,
        estilo: f.estilo,
        data: f.data,
        tags: f.tags.split(",").map((t) => t.trim()).filter(Boolean),
        cover,
        media: items.map(({ id, cat, legenda }) => ({ id, cat, legenda })),
      });
      setDirty(false);
      router.push(`/p/${p.code}?salvo=1`);
      router.refresh();
    } catch (e) {
      setError((e as Error).message);
      setBusy(false);
    }
  }

  return (
    <div className="editor">
      <div className="editor-bar">
        <div className="wrap">
          <div>
            <p className="eyebrow">Editando {p.code}</p>
            <div className="mono editor-name">{preview}</div>
          </div>
          <div className="editor-actions">
            {error && <span className="form-error">{error}</span>}
            <Link className="btn" href={`/p/${p.code}`}>Cancelar</Link>
            <button className="btn primary" onClick={save} disabled={busy}>{busy ? "Salvando…" : "Salvar"}</button>
          </div>
        </div>
      </div>

      <div className="wrap editor-body">
        <section className="editor-form">
          <h2 className="eyebrow">Ficha</h2>
          <label className="field wide">
            <span>Título (sem nome de cliente)</span>
            <input value={f.titulo} onChange={(e) => set("titulo", e.target.value)} maxLength={140} />
          </label>
          <label className="field wide">
            <span>Descrição</span>
            <textarea rows={4} value={f.descricao} onChange={(e) => set("descricao", e.target.value)} maxLength={2000} />
          </label>
          <div className="grid-fields">
            <label className="field"><span>Tipo</span>
              <select value={f.tipo} onChange={(e) => set("tipo", e.target.value as Tipo)}>
                {Object.entries(TIPOS).map(([k, v]) => <option key={k} value={k}>{k} — {v}</option>)}
              </select>
            </label>
            <label className="field"><span>Pavimentos</span>
              <select value={f.pavimentos} onChange={(e) => set("pavimentos", e.target.value as Pavimento)}>
                {Object.entries(PAVIMENTOS).map(([k, v]) => <option key={k} value={k}>{k} — {v}</option>)}
              </select>
            </label>
            <label className="field"><span>Terreno frente (m)</span><input inputMode="decimal" value={f.frente} onChange={(e) => set("frente", e.target.value)} placeholder="vazio = ND" /></label>
            <label className="field"><span>Terreno fundo (m)</span><input inputMode="decimal" value={f.fundo} onChange={(e) => set("fundo", e.target.value)} placeholder="vazio = ND" /></label>
            <label className="field"><span>Área construída (m²)</span><input inputMode="decimal" value={f.area} onChange={(e) => set("area", e.target.value)} placeholder="vazio = ND" /></label>
            <label className="field"><span>Suítes</span><input inputMode="numeric" value={f.suites} onChange={(e) => set("suites", e.target.value)} placeholder="vazio = ND" /></label>
            <label className="field"><span>Dormitórios</span><input inputMode="numeric" value={f.quartos} onChange={(e) => set("quartos", e.target.value)} /></label>
            <label className="field"><span>Banheiros</span><input inputMode="numeric" value={f.banheiros} onChange={(e) => set("banheiros", e.target.value)} /></label>
            <label className="field"><span>Vagas</span><input inputMode="numeric" value={f.vagas} onChange={(e) => set("vagas", e.target.value)} /></label>
            <label className="field"><span>Sistema construtivo</span><input value={f.sistema} onChange={(e) => set("sistema", e.target.value)} placeholder="Alvenaria, Steel frame…" /></label>
            <label className="field"><span>Estilo</span><input value={f.estilo} onChange={(e) => set("estilo", e.target.value)} /></label>
            <label className="field"><span>Data (AAAA-MM)</span><input value={f.data} onChange={(e) => set("data", e.target.value)} placeholder="2026-10" maxLength={7} /></label>
          </div>
          <label className="field wide">
            <span>Etiquetas (separadas por vírgula)</span>
            <input value={f.tags} onChange={(e) => set("tags", e.target.value)} placeholder="planta em L, re-render" />
          </label>
          <div className="checks">
            <label><input type="checkbox" checked={f.piscina} onChange={(e) => set("piscina", e.target.checked)} /> Piscina</label>
            <label><input type="checkbox" checked={f.gourmet} onChange={(e) => set("gourmet", e.target.checked)} /> Área gourmet</label>
            <label><input type="checkbox" checked={f.destaque} onChange={(e) => set("destaque", e.target.checked)} /> Destaque</label>
          </div>
          <div className="editor-danger">
            <DeleteButton code={p.code} />
          </div>
        </section>

        <section>
          <h2 className="eyebrow">Imagens · {items.length}</h2>
          <p className="hint">Ordem da galeria, categoria, legenda e capa. “Tirar” esconde a imagem deste projeto (dá para voltar abaixo).</p>
          <div className="media-list">
            {items.map((m, i) => (
              <div key={m.id} className={`media-row${cover === m.id ? " is-cover" : ""}`}>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={`/api/m/${m.id}/t`} alt="" loading="lazy" />
                <div className="media-fields">
                  <select value={m.cat} onChange={(e) => setItem(m.id, { cat: e.target.value as Categoria })} aria-label="Categoria">
                    {Object.entries(CATEGORIAS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
                  </select>
                  <input value={m.legenda} onChange={(e) => setItem(m.id, { legenda: e.target.value })} placeholder="Legenda" maxLength={80} aria-label="Legenda" />
                  <div className="media-btns">
                    <button type="button" className="chip" aria-pressed={cover === m.id} onClick={() => { setCover(m.id); setDirty(true); }}>{cover === m.id ? "★ Capa" : "Usar como capa"}</button>
                    <button type="button" className="icon-btn" onClick={() => move(i, -1)} disabled={i === 0} aria-label="Subir">↑</button>
                    <button type="button" className="icon-btn" onClick={() => move(i, 1)} disabled={i === items.length - 1} aria-label="Descer">↓</button>
                    <button type="button" className="chip" onClick={() => { setItems((l) => l.filter((x) => x.id !== m.id)); setDirty(true); }}>Tirar</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
          {removed.length > 0 && (
            <>
              <h2 className="eyebrow" style={{ marginTop: 28 }}>Imagens retiradas · {removed.length}</h2>
              <div className="media-removed">
                {removed.map((m) => (
                  <button
                    key={m.id}
                    type="button"
                    title="Voltar para o projeto"
                    onClick={() => { setItems((l) => [...l, { id: m.id, cat: m.cat, legenda: m.legenda ?? "", w: m.w, h: m.h }]); setDirty(true); }}
                  >
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={`/api/m/${m.id}/t`} alt="" loading="lazy" />
                    <span>+ voltar</span>
                  </button>
                ))}
              </div>
            </>
          )}
        </section>
      </div>
    </div>
  );
}
