#!/usr/bin/env node
// CLI do acervo Cobogó — tudo que entra no site passa por aqui.
//
//   npm run acervo:keygen                 gera VAULT_KEY e AUTH_SECRET novos
//   npm run acervo:user -- bruno          gera o hash de senha de um usuário (pede a senha)
//   npm run acervo:add -- incoming/minha-pasta [--dry]
//   npm run acervo:list
//   npm run acervo:edit -- CB004 area=162 suites=3 titulo="Casa térrea em L"
//   npm run acervo:remove -- CB004
//   npm run acervo:export                 descriptografa tudo em export/ (backup local)
//
// Estrutura de uma pasta de entrada (veja docs/PADRAO.md):
//   projeto.json
//   fachada/  interna/  planta/  layout/  implantacao/  cobertura/  corte/  outros/
// Aceita .jpg .jpeg .png .webp .tif e .pdf (cada página do PDF vira uma imagem).

import { createCipheriv, createDecipheriv, randomBytes, scrypt as scryptCb } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { createInterface } from "node:readline";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const VAULT = path.join(ROOT, "vault");
const MEDIA = path.join(VAULT, "media");
const CATALOG = path.join(VAULT, "catalog.enc");
const scrypt = promisify(scryptCb);

const CATS = ["fachada", "interna", "planta", "layout", "implantacao", "cobertura", "corte", "outros"];
const ALIASES = {
  fachadas: "fachada", externa: "fachada", externas: "fachada", exterior: "fachada", perspectiva: "fachada",
  internas: "interna", interior: "interna", interiores: "interna",
  "planta-baixa": "planta", planta_baixa: "planta", plantas: "planta", tecnica: "planta",
  humanizada: "layout", "planta-humanizada": "layout", layouts: "layout",
  situacao: "implantacao", cortes: "corte", elevacao: "corte", elevacoes: "corte",
};
const TIPOS = ["R", "H", "C", "I", "M"];
const PAVS = ["T", "TM", "S", "3P", "SS", "ND"];
const IMG_EXT = new Set([".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"]);

// ---------- env / cripto ----------
function loadEnv() {
  const f = path.join(ROOT, ".env");
  if (!existsSync(f)) return;
  for (const line of readFileSync(f, "utf8").split("\n")) {
    const m = line.match(/^\s*([A-Z_]+)\s*=\s*(.*)\s*$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, "");
  }
}
function key() {
  loadEnv();
  const k = Buffer.from(process.env.VAULT_KEY ?? "", "base64");
  if (k.length !== 32) die("VAULT_KEY ausente ou inválida. Coloque no arquivo acervo/.env (veja .env.example).");
  return k;
}
function encrypt(buf) {
  const iv = randomBytes(12);
  const c = createCipheriv("aes-256-gcm", key(), iv);
  const ct = Buffer.concat([c.update(buf), c.final()]);
  return Buffer.concat([iv, c.getAuthTag(), ct]);
}
function decrypt(buf) {
  const d = createDecipheriv("aes-256-gcm", key(), buf.subarray(0, 12));
  d.setAuthTag(buf.subarray(12, 28));
  return Buffer.concat([d.update(buf.subarray(28)), d.final()]);
}
function readCatalog() {
  if (!existsSync(CATALOG)) return { version: 1, updated: new Date().toISOString(), projects: [] };
  return JSON.parse(decrypt(readFileSync(CATALOG)).toString("utf8"));
}
function writeCatalog(cat) {
  cat.updated = new Date().toISOString();
  cat.projects.sort((a, b) => a.code.localeCompare(b.code));
  mkdirSync(VAULT, { recursive: true });
  writeFileSync(CATALOG, encrypt(Buffer.from(JSON.stringify(cat))));
}

// ---------- padrão de nome ----------
const fmt = (n) => (Number.isInteger(n) ? String(n) : n.toFixed(1));
export function buildName(p) {
  const t = p.terreno ? `${fmt(p.terreno.frente)}X${fmt(p.terreno.fundo)}` : "ND";
  const s = p.suites == null ? "NDSUITES" : p.suites === 1 ? "1SUITE" : `${p.suites}SUITES`;
  const a = p.area == null ? "NDM2" : `${Math.round(p.area)}M2`;
  return ["ARQ", p.tipo, t, p.pavimentos, a, s].join("_");
}
function nextCode(cat) {
  const max = cat.projects.reduce((m, p) => Math.max(m, parseInt(p.code.slice(2), 10) || 0), 0);
  return `CB${String(max + 1).padStart(3, "0")}`;
}

function validate(meta) {
  const errs = [];
  if (!TIPOS.includes(meta.tipo)) errs.push(`tipo deve ser um de ${TIPOS.join(", ")}`);
  if (!PAVS.includes(meta.pavimentos)) errs.push(`pavimentos deve ser um de ${PAVS.join(", ")}`);
  if (meta.area !== null && !(meta.area > 0)) errs.push("area (m²) deve ser número > 0 ou null (a confirmar)");
  if (meta.suites !== null && (!Number.isInteger(meta.suites) || meta.suites < 0)) errs.push("suites deve ser inteiro ≥ 0 ou null (a confirmar)");
  if (meta.terreno !== null && !(meta.terreno?.frente > 0 && meta.terreno?.fundo > 0))
    errs.push('terreno deve ser {"frente": 15, "fundo": 20} ou null');
  if (!meta.titulo) errs.push("titulo (descritivo, sem nome de cliente) obrigatório");
  return errs;
}

// ---------- imagens ----------
async function sharp() {
  try {
    return (await import("sharp")).default;
  } catch {
    die("Instale as dependências: npm install (o sharp é usado para otimizar as imagens).");
  }
}

function catOf(dirName, fileName) {
  const norm = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/^\d+[\s._-]*/, "");
  const d = norm(dirName);
  if (CATS.includes(d)) return d;
  if (ALIASES[d]) return ALIASES[d];
  const prefix = norm(fileName).split(/__|--/)[0];
  if (CATS.includes(prefix)) return prefix;
  if (ALIASES[prefix]) return ALIASES[prefix];
  return null;
}

function collect(dir) {
  const out = [];
  const walk = (d, cat) => {
    for (const name of readdirSync(d).sort((a, b) => a.localeCompare(b, "pt", { numeric: true }))) {
      const full = path.join(d, name);
      if (statSync(full).isDirectory()) walk(full, catOf(name, "") ?? cat);
      else {
        const ext = path.extname(name).toLowerCase();
        if (!IMG_EXT.has(ext) && ext !== ".pdf") continue;
        const c = catOf(path.basename(d), name) ?? cat;
        out.push({ file: full, cat: c ?? "outros", ext, legenda: legendaDe(name) });
      }
    }
  };
  walk(dir, null);
  return out;
}

function legendaDe(name) {
  return path
    .basename(name, path.extname(name))
    .replace(/^[a-z]+(__|--)/i, "")
    .replace(/^\d+[\s._-]*/, "")
    .replace(/\bcapa\b/i, "")
    .replace(/[_-]+/g, " ")
    .trim()
    .slice(0, 80);
}

function pdfToPngs(pdf) {
  const tmp = mkdtempSync(path.join(tmpdir(), "cb-pdf-"));
  execFileSync("pdftoppm", ["-r", "200", "-png", pdf, path.join(tmp, "p")]);
  return { tmp, files: readdirSync(tmp).sort().map((f) => path.join(tmp, f)) };
}

async function ingestImage(S, input, item) {
  const id = randomBytes(8).toString("hex");
  // .rotate() aplica a orientação EXIF; o sharp descarta metadados (GPS, autor, software) por padrão
  const base = S(input, { limitInputPixels: false }).rotate();
  const full = await base.clone().resize({ width: 2400, height: 2400, fit: "inside", withoutEnlargement: true }).webp({ quality: 82 }).toBuffer({ resolveWithObject: true });
  const thumb = await base.clone().resize({ width: 960, height: 960, fit: "inside", withoutEnlargement: true }).webp({ quality: 72 }).toBuffer();
  mkdirSync(MEDIA, { recursive: true });
  writeFileSync(path.join(MEDIA, `${id}.f.enc`), encrypt(full.data));
  writeFileSync(path.join(MEDIA, `${id}.t.enc`), encrypt(thumb));
  return { id, cat: item.cat, w: full.info.width, h: full.info.height, ...(item.legenda ? { legenda: item.legenda } : {}), ...(item.rerender ? { rerender: true } : {}) };
}

// ---------- comandos ----------
async function cmdAdd(dir, flags) {
  if (!dir || !existsSync(dir)) die("Informe a pasta: npm run acervo:add -- incoming/minha-pasta");
  const metaFile = path.join(dir, "projeto.json");
  if (!existsSync(metaFile)) die(`Faltou ${metaFile} (copie de docs/projeto.exemplo.json)`);
  const meta = JSON.parse(readFileSync(metaFile, "utf8"));
  for (const k of ["terreno", "area", "suites"]) if (meta[k] === undefined) meta[k] = null;
  const errs = validate(meta);
  if (errs.length) die("projeto.json inválido:\n  - " + errs.join("\n  - "));

  const items = collect(dir);
  if (!items.length) die("Nenhuma imagem/PDF encontrado nas subpastas.");
  const name = buildName(meta);
  const cat = readCatalog();
  const code = meta.code ?? nextCode(cat);
  if (cat.projects.some((p) => p.code === code)) die(`${code} já existe — use acervo:edit ou remova antes.`);

  console.log(`\n${code}  ${name}\n${meta.titulo}`);
  const byCat = items.reduce((m, i) => ((m[i.cat] = (m[i.cat] ?? 0) + 1), m), {});
  console.log("Arquivos:", byCat);
  const faltando = ["fachada", "interna", "planta", "layout"].filter((c) => !byCat[c]);
  if (faltando.length) console.log("⚠ Sem:", faltando.join(", "));
  if (flags.dry) return console.log("(--dry: nada gravado)");

  const S = await sharp();
  const media = [];
  for (const it of items) {
    if (it.ext === ".pdf") {
      const { tmp, files } = pdfToPngs(it.file);
      for (const [i, f] of files.entries()) media.push(await ingestImage(S, f, { ...it, legenda: `${it.legenda} ${files.length > 1 ? i + 1 : ""}`.trim() }));
      rmSync(tmp, { recursive: true, force: true });
    } else {
      media.push(await ingestImage(S, it.file, { ...it, rerender: /rerender|render-ia/i.test(it.file) }));
    }
    process.stdout.write(".");
  }
  const capa = items.findIndex((i) => /capa[^\\/]*$/i.test(i.file));
  const projeto = {
    ...meta,
    code,
    name,
    cover: capa >= 0 ? media[capa]?.id : media.find((m) => m.cat === "fachada")?.id ?? media[0].id,
    media,
  };
  delete projeto.$schema;
  cat.projects.push(projeto);
  writeCatalog(cat);
  console.log(`\n✔ ${code} adicionado com ${media.length} imagens. Faça commit de vault/ e o deploy atualiza sozinho.`);
}

function cmdList() {
  const cat = readCatalog();
  console.log(`${cat.projects.length} projetos · atualizado ${cat.updated}\n`);
  for (const p of cat.projects) {
    const c = p.media.reduce((m, x) => ((m[x.cat] = (m[x.cat] ?? 0) + 1), m), {});
    console.log(`${p.code}  ${p.name.padEnd(42)} ${String(p.media.length).padStart(3)} img  F${c.fachada ?? 0} I${c.interna ?? 0} P${c.planta ?? 0} L${c.layout ?? 0}  ${p.titulo}`);
  }
}

function parseValue(v) {
  if (v === "null") return null;
  if (v === "true" || v === "false") return v === "true";
  if (/^-?\d+(\.\d+)?$/.test(v)) return Number(v);
  if (/^\d+(\.\d+)?x\d+(\.\d+)?$/i.test(v)) {
    const [frente, fundo] = v.toLowerCase().split("x").map(Number);
    return { frente, fundo };
  }
  if (v.startsWith("[") || v.startsWith("{")) return JSON.parse(v);
  return v;
}

function cmdEdit(code, pairs) {
  const cat = readCatalog();
  const p = cat.projects.find((x) => x.code === code);
  if (!p) die(`${code} não encontrado`);
  for (const pair of pairs) {
    const i = pair.indexOf("=");
    if (i < 0) die(`Use chave=valor (recebi "${pair}")`);
    const k = pair.slice(0, i);
    if (["code", "media", "name"].includes(k)) die(`"${k}" não é editável`);
    p[k] = parseValue(pair.slice(i + 1));
  }
  const errs = validate(p);
  if (errs.length) die("Resultado inválido:\n  - " + errs.join("\n  - "));
  p.name = buildName(p);
  writeCatalog(cat);
  console.log(`✔ ${p.code}  ${p.name}`);
}

function cmdRemove(code) {
  const cat = readCatalog();
  const p = cat.projects.find((x) => x.code === code);
  if (!p) die(`${code} não encontrado`);
  for (const m of p.media) for (const s of ["t", "f"]) rmSync(path.join(MEDIA, `${m.id}.${s}.enc`), { force: true });
  cat.projects = cat.projects.filter((x) => x !== p);
  writeCatalog(cat);
  console.log(`✔ ${code} removido (o código não será reutilizado se houver projetos posteriores)`);
}

function cmdExport() {
  const cat = readCatalog();
  const out = path.join(ROOT, "export");
  for (const p of cat.projects) {
    const d = path.join(out, `${p.code}_${p.name}`);
    mkdirSync(d, { recursive: true });
    const { media, ...meta } = p;
    writeFileSync(path.join(d, "projeto.json"), JSON.stringify(meta, null, 2));
    const n = {};
    for (const m of media) {
      n[m.cat] = (n[m.cat] ?? 0) + 1;
      writeFileSync(path.join(d, `${m.cat}_${String(n[m.cat]).padStart(2, "0")}.webp`), decrypt(readFileSync(path.join(MEDIA, `${m.id}.f.enc`))));
    }
  }
  console.log(`✔ ${cat.projects.length} projetos exportados para export/ (pasta ignorada pelo git)`);
}

function cmdKeygen() {
  console.log(`VAULT_KEY=${randomBytes(32).toString("base64")}`);
  console.log(`AUTH_SECRET=${randomBytes(48).toString("base64url")}`);
  console.log("\nGuarde em local seguro. Trocar a VAULT_KEY exige recriptografar o cofre.");
}

async function cmdUser(name) {
  if (!name) die("Informe o usuário: npm run acervo:user -- rafael");
  const pw = process.env.SENHA ?? (await ask(`Senha para ${name}: `));
  if (pw.length < 10) die("Use pelo menos 10 caracteres.");
  const salt = randomBytes(16);
  const N = 16384, r = 8, p = 1;
  const hash = await scrypt(pw, salt, 32, { N, r, p });
  console.log(`${name.toLowerCase()}:scrypt.${N}.${r}.${p}.${salt.toString("base64")}.${hash.toString("base64")}`);
  console.log("\nJunte as linhas com ';' na variável AUTH_USERS do servidor.");
}

function ask(q) {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((res) => rl.question(q, (a) => (rl.close(), res(a))));
}
function die(msg) {
  console.error(`✖ ${msg}`);
  process.exit(1);
}

const [cmd, ...rest] = process.argv.slice(2);
const flags = Object.fromEntries(rest.filter((a) => a.startsWith("--")).map((a) => [a.slice(2), true]));
const args = rest.filter((a) => !a.startsWith("--"));
const run = { add: () => cmdAdd(args[0], flags), list: cmdList, edit: () => cmdEdit(args[0], args.slice(1)), remove: () => cmdRemove(args[0]), export: cmdExport, keygen: cmdKeygen, user: () => cmdUser(args[0]) }[cmd];
if (!run) die("Comandos: add | list | edit | remove | export | keygen | user");
await run();
