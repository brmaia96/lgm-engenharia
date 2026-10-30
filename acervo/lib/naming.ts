// Padrão de nomenclatura do acervo.
//
//   ARQ _ R _ 15X20 _ T _ 150M2 _ 3SUITES
//   │     │   │       │   │       └─ quantidade de suítes
//   │     │   │       │   └───────── área total construída
//   │     │   │       └───────────── pavimentos
//   │     │   └───────────────────── terreno frente x fundo (m) — "ND" quando não definido
//   │     └───────────────────────── tipo
//   └─────────────────────────────── disciplina (arquitetura)
//
// O código curto (CB001, CB002…) é sequencial, único e nunca muda.

import type { Categoria, Pavimento, Projeto, Tipo } from "./types";

export const TIPOS: Record<Tipo, string> = {
  R: "Residencial",
  H: "Hospedagem / Chalé",
  C: "Comercial",
  I: "Institucional",
  M: "Misto",
};

export const PAVIMENTOS: Record<Pavimento, string> = {
  T: "Térreo",
  TM: "Térreo + mezanino",
  S: "Sobrado",
  "3P": "3 pavimentos",
  SS: "Com subsolo",
  ND: "A confirmar",
};

export const CATEGORIAS: Record<Categoria, string> = {
  fachada: "Fachadas",
  interna: "Internas",
  planta: "Planta baixa",
  layout: "Layout",
  implantacao: "Implantação",
  cobertura: "Cobertura",
  corte: "Cortes",
  outros: "Outros",
};

/** as quatro categorias que todo projeto deve ter */
export const CATEGORIAS_ESSENCIAIS: Categoria[] = ["fachada", "interna", "planta", "layout"];

function fmt(n: number) {
  return Number.isInteger(n) ? String(n) : n.toFixed(1);
}

export function terrenoLabel(t: Projeto["terreno"]) {
  return t ? `${fmt(t.frente)}X${fmt(t.fundo)}` : "ND";
}

export function buildName(p: Pick<Projeto, "tipo" | "terreno" | "pavimentos" | "area" | "suites">) {
  const suites = p.suites == null ? "NDSUITES" : p.suites === 1 ? "1SUITE" : `${p.suites}SUITES`;
  const area = p.area == null ? "NDM2" : `${Math.round(p.area)}M2`;
  return ["ARQ", p.tipo, terrenoLabel(p.terreno), p.pavimentos, area, suites].join("_");
}

/** campos que ainda precisam ser confirmados */
export function pendencias(p: Pick<Projeto, "area" | "suites" | "terreno">) {
  const out: string[] = [];
  if (p.area == null) out.push("área");
  if (p.suites == null) out.push("suítes");
  if (p.terreno == null) out.push("terreno");
  return out;
}

export function buildCode(seq: number) {
  return `CB${String(seq).padStart(3, "0")}`;
}
