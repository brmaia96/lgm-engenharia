"use client";
import { useRouter } from "next/navigation";
import { useRef, useState } from "react";
import { buildName, CATEGORIAS, PAVIMENTOS, TIPOS } from "@/lib/naming";
import type { Categoria, Pavimento, Tipo } from "@/lib/types";
import { call } from "./ProjectActions";

type Up = { key: string; name: string; status: "enviando" | "ok" | "erro"; id?: string; cat: Categoria; legenda: string; w: number; h: number; preview: string; erro?: string };

// Otimiza no navegador: versão grande (até 2400 px) e miniatura (960 px), em WebP.
async function toWebp(file: File, max: number, quality: number) {
  const bmp = await createImageBitmap(file, { imageOrientation: "from-image" });
  const scale = Math.min(1, max / Math.max(bmp.width, bmp.height));
  const w = Math.round(bmp.width * scale);
  const h = Math.round(bmp.height * scale);
  const canvas = document.createElement("canvas");
  canvas.width = w;
  canvas.height = h;
  canvas.getContext("2d")!.drawImage(bmp, 0, 0, w, h);
  const blob = await new Promise<Blob>((res, rej) => canvas.toBlob((b) => (b ? res(b) : rej(new Error("falha ao converter"))), "image/webp", quality));
  return { blob, w, h };
}

const guessCat = (name: string): Categoria => {
  const n = name.toLowerCase();
  if (/intern|sala|cozinha|quarto|suite|banho|living/.test(n)) return "interna";
  if (/humaniz|layout/.test(n)) return "layout";
  if (/planta|baixa/.test(n)) return "planta";
  if (/corte|eleva/.test(n)) return "corte";
  if (/implanta/.test(n)) return "implantacao";
  return "fachada";
};

const toNum = (s: string) => (s.trim() === "" ? null : Number(s.replace(",", ".")));

export function NewProject() {
  const router = useRouter();
  const input = useRef<HTMLInputElement>(null);
  const [ups, setUps] = useState<Up[]>([]);
  const [cover, setCover] = useState("");
  const [drag, setDrag] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [f, setF] = useState({ titulo: "", descricao: "", tipo: "R" as Tipo, pavimentos: "T" as Pavimento, frente: "", fundo: "", area: "", suites: "", quartos: "", banheiros: "", vagas: "", sistema: "", estilo: "", data: "", piscina: false, gourmet: false });
  const set = <K extends keyof typeof f>(k: K, v: (typeof f)[K]) => setF((s) => ({ ...s, [k]: v }));
  const patch = (key: string, p: Partial<Up>) => setUps((l) => l.map((u) => (u.key === key ? { ...u, ...p } : u)));

  async function add(files: FileList | File[]) {
    for (const file of Array.from(files)) {
      if (!file.type.startsWith("image/")) continue;
      const key = `${file.name}-${file.size}-${Math.random()}`;
      setUps((l) => [...l, { key, name: file.name, status: "enviando", cat: guessCat(file.name), legenda: "", w: 0, h: 0, preview: URL.createObjectURL(file) }]);
      try {
        const big = await toWebp(file, 2400, 0.84);
        const small = await toWebp(file, 960, 0.74);
        const fd = new FormData();
        fd.append("f", big.blob, "f.webp");
        fd.append("t", small.blob, "t.webp");
        const res = await fetch("/api/midia", { method: "POST", body: fd });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(data.error ?? `Erro ${res.status}`);
        patch(key, { status: "ok", id: data.id, w: big.w, h: big.h });
        setCover((c) => c || data.id);
      } catch (e) {
        patch(key, { status: "erro", erro: (e as Error).message });
      }
    }
  }

  const ok = ups.filter((u) => u.status === "ok");
  const terreno = toNum(f.frente) && toNum(f.fundo) ? { frente: toNum(f.frente)!, fundo: toNum(f.fundo)! } : null;
  const preview = buildName({ tipo: f.tipo, pavimentos: f.pavimentos, terreno, area: toNum(f.area), suites: toNum(f.suites) });

  async function create() {
    setError("");
    if (!f.titulo.trim()) return setError("Dê um título (sem nome de cliente).");
    if (!ok.length) return setError("Envie pelo menos uma imagem.");
    if (ups.some((u) => u.status === "enviando")) return setError("Aguarde o envio das imagens terminar.");
    setBusy(true);
    try {
      const r = await call("/api/projetos", "POST", {
        ...f, terreno, area: toNum(f.area), suites: toNum(f.suites), quartos: toNum(f.quartos), banheiros: toNum(f.banheiros), vagas: toNum(f.vagas),
        tags: [], cover, media: ok.map((u) => ({ id: u.id, cat: u.cat, legenda: u.legenda, w: u.w, h: u.h })),
      });
      router.push(`/p/${r.projects[0].code}?salvo=1`);
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
            <p className="eyebrow">Novo projeto</p>
            <div className="editor-name">{preview}</div>
          </div>
          <div className="editor-actions">
            {error && <span className="form-error">{error}</span>}
            <button className="btn primary" onClick={create} disabled={busy}>{busy ? "Criando…" : "Criar projeto"}</button>
          </div>
        </div>
      </div>
      <div className="wrap editor-body">
        <section className="editor-form">
          <label className="field wide"><span>Título (sem nome de cliente)</span><input value={f.titulo} onChange={(e) => set("titulo", e.target.value)} maxLength={140} placeholder="Casa térrea com piscina" /></label>
          <label className="field wide"><span>Descrição</span><textarea rows={3} value={f.descricao} onChange={(e) => set("descricao", e.target.value)} maxLength={2000} /></label>
          <div className="grid-fields">
            <label className="field"><span>Tipo</span><select value={f.tipo} onChange={(e) => set("tipo", e.target.value as Tipo)}>{Object.entries(TIPOS).map(([k, v]) => <option key={k} value={k}>{k} — {v}</option>)}</select></label>
            <label className="field"><span>Pavimentos</span><select value={f.pavimentos} onChange={(e) => set("pavimentos", e.target.value as Pavimento)}>{Object.entries(PAVIMENTOS).map(([k, v]) => <option key={k} value={k}>{k} — {v}</option>)}</select></label>
            <label className="field"><span>Terreno frente (m)</span><input inputMode="decimal" value={f.frente} onChange={(e) => set("frente", e.target.value)} placeholder="vazio = ND" /></label>
            <label className="field"><span>Terreno fundo (m)</span><input inputMode="decimal" value={f.fundo} onChange={(e) => set("fundo", e.target.value)} placeholder="vazio = ND" /></label>
            <label className="field"><span>Área construída (m²)</span><input inputMode="decimal" value={f.area} onChange={(e) => set("area", e.target.value)} placeholder="vazio = ND" /></label>
            <label className="field"><span>Suítes</span><input inputMode="numeric" value={f.suites} onChange={(e) => set("suites", e.target.value)} placeholder="vazio = ND" /></label>
            <label className="field"><span>Dormitórios</span><input inputMode="numeric" value={f.quartos} onChange={(e) => set("quartos", e.target.value)} /></label>
            <label className="field"><span>Banheiros</span><input inputMode="numeric" value={f.banheiros} onChange={(e) => set("banheiros", e.target.value)} /></label>
            <label className="field"><span>Vagas</span><input inputMode="numeric" value={f.vagas} onChange={(e) => set("vagas", e.target.value)} /></label>
            <label className="field"><span>Sistema</span><input value={f.sistema} onChange={(e) => set("sistema", e.target.value)} placeholder="Alvenaria, Steel frame…" /></label>
            <label className="field"><span>Estilo</span><input value={f.estilo} onChange={(e) => set("estilo", e.target.value)} /></label>
            <label className="field"><span>Data (AAAA-MM)</span><input value={f.data} onChange={(e) => set("data", e.target.value)} placeholder="2026-11" maxLength={7} /></label>
          </div>
          <div className="checks">
            <label><input type="checkbox" checked={f.piscina} onChange={(e) => set("piscina", e.target.checked)} /> Piscina</label>
            <label><input type="checkbox" checked={f.gourmet} onChange={(e) => set("gourmet", e.target.checked)} /> Área gourmet</label>
          </div>
        </section>

        <section>
          <div
            className={`dropzone${drag ? " over" : ""}`}
            onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
            onDragLeave={() => setDrag(false)}
            onDrop={(e) => { e.preventDefault(); setDrag(false); add(e.dataTransfer.files); }}
            onClick={() => input.current?.click()}
            role="button"
            tabIndex={0}
          >
            <p className="dz-title">Arraste as imagens aqui</p>
            <p className="hint" style={{ margin: 0 }}>ou clique para escolher · fachadas, internas, planta baixa e layout · JPG ou PNG</p>
            <p className="hint" style={{ margin: 0 }}>Antes de enviar, confira que não há nome de cliente, endereço ou carimbo nas imagens.</p>
            <input ref={input} type="file" accept="image/*" multiple hidden onChange={(e) => e.target.files && add(e.target.files)} />
          </div>
          {ups.length > 0 && (
            <div className="media-list" style={{ marginTop: 18 }}>
              {ups.map((u) => (
                <div key={u.key} className={`media-row${cover && cover === u.id ? " is-cover" : ""}`}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={u.preview} alt="" />
                  <div className="media-fields">
                    <span className="hint" style={{ margin: 0 }}>{u.status === "enviando" ? "Otimizando e enviando…" : u.status === "erro" ? `Erro: ${u.erro}` : "Enviada"}</span>
                    <select value={u.cat} onChange={(e) => patch(u.key, { cat: e.target.value as Categoria })} aria-label="Categoria">
                      {Object.entries(CATEGORIAS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
                    </select>
                    <input value={u.legenda} onChange={(e) => patch(u.key, { legenda: e.target.value })} placeholder="Legenda (opcional)" maxLength={80} />
                    <div className="media-btns">
                      {u.id && <button type="button" className="chip" aria-pressed={cover === u.id} onClick={() => setCover(u.id!)}>{cover === u.id ? "★ Capa" : "Usar como capa"}</button>}
                      <button type="button" className="chip" onClick={() => setUps((l) => l.filter((x) => x.key !== u.key))}>Remover</button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
