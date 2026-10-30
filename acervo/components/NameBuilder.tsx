"use client";
import { useState } from "react";
import { buildName, PAVIMENTOS, TIPOS } from "@/lib/naming";
import type { Pavimento, Tipo } from "@/lib/types";
import { CopyButton } from "./CopyButton";

export function NameBuilder() {
  const [tipo, setTipo] = useState<Tipo>("R");
  const [frente, setFrente] = useState("15");
  const [fundo, setFundo] = useState("20");
  const [pav, setPav] = useState<Pavimento>("T");
  const [area, setArea] = useState("150");
  const [suites, setSuites] = useState("3");
  const terreno = Number(frente) > 0 && Number(fundo) > 0 ? { frente: Number(frente), fundo: Number(fundo) } : null;
  const name = buildName({ tipo, terreno, pavimentos: pav, area: Number(area) || 0, suites: Number(suites) || 0 });
  const json = JSON.stringify({ tipo, terreno, pavimentos: pav, area: Number(area) || 0, suites: Number(suites) || 0, titulo: "Casa térrea com 3 suítes" }, null, 2);

  return (
    <div className="namebox">
      <div className="nameout mono" aria-live="polite">
        {name.split("_").map((part, i) => <span key={i}>{part}{i < 5 ? "_" : ""}</span>)}
      </div>
      <div className="builder">
        <label>Tipo<select value={tipo} onChange={(e) => setTipo(e.target.value as Tipo)}>{Object.entries(TIPOS).map(([k, v]) => <option key={k} value={k}>{k} — {v}</option>)}</select></label>
        <label>Frente (m)<input inputMode="decimal" value={frente} onChange={(e) => setFrente(e.target.value)} placeholder="vazio = ND" /></label>
        <label>Fundo (m)<input inputMode="decimal" value={fundo} onChange={(e) => setFundo(e.target.value)} /></label>
        <label>Pavimentos<select value={pav} onChange={(e) => setPav(e.target.value as Pavimento)}>{Object.entries(PAVIMENTOS).map(([k, v]) => <option key={k} value={k}>{k} — {v}</option>)}</select></label>
        <label>Área (m²)<input inputMode="numeric" value={area} onChange={(e) => setArea(e.target.value)} /></label>
        <label>Suítes<input inputMode="numeric" value={suites} onChange={(e) => setSuites(e.target.value)} /></label>
      </div>
      <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
        <span className="eyebrow">projeto.json correspondente</span>
        <span className="codebar" style={{ background: "var(--grafite)", color: "#ece6da" }}><CopyButton text={json} /></span>
      </div>
      <pre className="tree">{json}</pre>
    </div>
  );
}
