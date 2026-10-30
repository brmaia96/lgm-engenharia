"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { CATEGORIAS, CATEGORIAS_ESSENCIAIS } from "@/lib/naming";
import type { Categoria, Midia } from "@/lib/types";

const ORDER: Categoria[] = ["fachada", "interna", "planta", "layout", "implantacao", "cobertura", "corte", "outros"];

export function Gallery({ media, baseName }: { media: Midia[]; baseName: string }) {
  const present = ORDER.filter((c) => media.some((m) => m.cat === c));
  const tabs: (Categoria | "todas")[] = ["todas", ...ORDER.filter((c) => CATEGORIAS_ESSENCIAIS.includes(c) || present.includes(c))];
  const [tab, setTab] = useState<Categoria | "todas">("todas");
  const [open, setOpen] = useState<number | null>(null);

  const list = (tab === "todas" ? [...media].sort((a, b) => ORDER.indexOf(a.cat) - ORDER.indexOf(b.cat)) : media.filter((m) => m.cat === tab));

  return (
    <div>
      <div className="tabs" role="tablist">
        {tabs.map((t) => {
          const n = t === "todas" ? media.length : media.filter((m) => m.cat === t).length;
          return (
            <button key={t} role="tab" aria-selected={tab === t} disabled={!n} onClick={() => setTab(t)}>
              {t === "todas" ? "Todas" : CATEGORIAS[t]}<small>{n}</small>
            </button>
          );
        })}
      </div>
      {list.length === 0 ? (
        <div className="missing">Sem imagens nesta categoria ainda.</div>
      ) : (
        <div className="gallery">
          {list.map((m, i) => (
            <button key={m.id} onClick={() => setOpen(i)} aria-label={`Abrir ${m.legenda ?? CATEGORIAS[m.cat]}`}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={`/api/m/${m.id}/t`} width={m.w} height={m.h} alt={m.legenda ?? CATEGORIAS[m.cat]} loading={i < 4 ? "eager" : "lazy"} decoding="async" style={{ aspectRatio: `${m.w}/${m.h}` }} />
              {m.rerender && <span className="badge-ia">RE-RENDER</span>}
              <figcaption>{CATEGORIAS[m.cat]}{m.legenda ? ` · ${m.legenda}` : ""}</figcaption>
            </button>
          ))}
        </div>
      )}
      {open !== null && <Lightbox items={list} start={open} onClose={() => setOpen(null)} baseName={baseName} />}
    </div>
  );
}

function Lightbox({ items, start, onClose, baseName }: { items: Midia[]; start: number; onClose: () => void; baseName: string }) {
  const [i, setI] = useState(start);
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const drag = useRef<{ x: number; y: number; px: number; py: number; moved: boolean } | null>(null);
  const touch = useRef<number | null>(null);
  const stripRef = useRef<HTMLDivElement>(null);
  const m = items[i];

  const go = useCallback((d: number) => {
    setI((v) => (v + d + items.length) % items.length);
    setZoom(1);
    setPan({ x: 0, y: 0 });
  }, [items.length]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
      if (e.key === "ArrowRight") go(1);
      if (e.key === "ArrowLeft") go(-1);
    };
    window.addEventListener("keydown", onKey);
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { window.removeEventListener("keydown", onKey); document.body.style.overflow = prev; };
  }, [go, onClose]);

  useEffect(() => {
    stripRef.current?.querySelector('[aria-current="true"]')?.scrollIntoView({ block: "nearest", inline: "center", behavior: "smooth" });
    // pré-carrega vizinhas
    for (const d of [1, -1]) new Image().src = `/api/m/${items[(i + d + items.length) % items.length].id}/f`;
  }, [i, items]);

  const n = String(i + 1).padStart(2, "0");
  return (
    <div className="lb" role="dialog" aria-modal="true" aria-label="Visualizador de imagens">
      <div className="lb-top">
        <span className="mono">{n} / {String(items.length).padStart(2, "0")}</span>
        <span>{CATEGORIAS[m.cat]}{m.legenda ? ` · ${m.legenda}` : ""}</span>
        <div className="sp">
          <button onClick={() => { setZoom((z) => (z > 1 ? 1 : 2.2)); setPan({ x: 0, y: 0 }); }} aria-label="Zoom" title="Zoom (clique na imagem)">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><circle cx="11" cy="11" r="7" /><path d="m20 20-3.5-3.5M8 11h6M11 8v6" /></svg>
          </button>
          <a href={`/api/m/${m.id}/f?dl=${encodeURIComponent(`${baseName}_${m.cat}_${n}`)}`} aria-label="Baixar" title="Baixar imagem">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><path d="M12 4v12m0 0-5-5m5 5 5-5M5 20h14" /></svg>
          </a>
          <button onClick={onClose} aria-label="Fechar" title="Fechar (Esc)">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><path d="M6 6l12 12M18 6 6 18" /></svg>
          </button>
        </div>
      </div>
      <div
        className={`lb-stage${zoom > 1 ? " zoomed" : ""}`}
        onPointerDown={(e) => { drag.current = { x: e.clientX, y: e.clientY, px: pan.x, py: pan.y, moved: false }; touch.current = e.clientX; }}
        onPointerMove={(e) => {
          const d = drag.current;
          if (!d) return;
          if (Math.abs(e.clientX - d.x) + Math.abs(e.clientY - d.y) > 6) d.moved = true;
          if (zoom > 1) setPan({ x: d.px + (e.clientX - d.x) / zoom, y: d.py + (e.clientY - d.y) / zoom });
        }}
        onPointerUp={(e) => {
          const d = drag.current;
          drag.current = null;
          if (!d) return;
          const dx = e.clientX - d.x;
          if (zoom === 1 && Math.abs(dx) > 50) return go(dx < 0 ? 1 : -1);
          if (!d.moved && (e.target as HTMLElement).tagName === "IMG") {
            setZoom((z) => (z > 1 ? 1 : 2.2));
            setPan({ x: 0, y: 0 });
          } else if (!d.moved && (e.target as HTMLElement).classList.contains("lb-stage")) onClose();
        }}
        onWheel={(e) => setZoom((z) => Math.min(5, Math.max(1, z - e.deltaY * 0.002)))}
      >
        {items.length > 1 && <button className="lb-arrow l" onClick={() => go(-1)} aria-label="Anterior">‹</button>}
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          key={m.id}
          src={`/api/m/${m.id}/f`}
          alt={m.legenda ?? CATEGORIAS[m.cat]}
          draggable={false}
          style={{ transform: `scale(${zoom}) translate(${pan.x}px, ${pan.y}px)`, backgroundImage: `url(/api/m/${m.id}/t)`, backgroundSize: "contain", backgroundRepeat: "no-repeat", backgroundPosition: "center" }}
        />
        {items.length > 1 && <button className="lb-arrow r" onClick={() => go(1)} aria-label="Próxima">›</button>}
      </div>
      <div className="lb-strip" ref={stripRef}>
        {items.map((it, k) => (
          <button key={it.id} aria-current={k === i} onClick={() => { setI(k); setZoom(1); setPan({ x: 0, y: 0 }); }} aria-label={`Imagem ${k + 1}`}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={`/api/m/${it.id}/t`} alt="" loading="lazy" />
          </button>
        ))}
      </div>
    </div>
  );
}
