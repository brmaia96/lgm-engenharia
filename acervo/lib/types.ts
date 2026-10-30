// Modelo de dados do acervo. O catálogo inteiro vive criptografado em vault/catalog.enc.

export type Tipo = "R" | "C" | "H" | "I" | "M";
export type Pavimento = "T" | "TM" | "S" | "3P" | "SS";
export type Categoria =
  | "fachada"
  | "interna"
  | "planta"
  | "layout"
  | "implantacao"
  | "cobertura"
  | "corte"
  | "outros";

export interface Midia {
  /** id aleatório (hex) — nunca deriva do nome do arquivo ou do cliente */
  id: string;
  cat: Categoria;
  w: number;
  h: number;
  legenda?: string;
  /** imagem re-renderizada / gerada a partir do projeto original */
  rerender?: boolean;
}

export interface Projeto {
  /** código curto e estável, ex.: CB007 */
  code: string;
  /** nome padronizado, ex.: ARQ_R_15X20_T_150M2_3SUITES */
  name: string;
  tipo: Tipo;
  /** frente x fundo do terreno em metros; null quando não se aplica (modelo de catálogo) */
  terreno: { frente: number; fundo: number } | null;
  pavimentos: Pavimento;
  /** área total construída, m² — null = a confirmar */
  area: number | null;
  /** null = a confirmar */
  suites: number | null;
  quartos?: number;
  banheiros?: number;
  vagas?: number;
  piscina?: boolean;
  gourmet?: boolean;
  sistema?: string;
  estilo?: string;
  /** título descritivo neutro, sem nome de cliente */
  titulo: string;
  descricao?: string;
  tags?: string[];
  destaque?: boolean;
  /** AAAA-MM do projeto */
  data?: string;
  cover?: string;
  media: Midia[];
}

export interface Catalogo {
  version: 1;
  updated: string;
  projects: Projeto[];
}

/** versão enviada ao navegador na listagem (sem a lista completa de mídias) */
export interface ProjetoResumo extends Omit<Projeto, "media"> {
  counts: Partial<Record<Categoria, number>>;
  thumbs: string[];
}
