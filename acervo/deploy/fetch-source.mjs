// Baixa o tarball do repositório (só código + acervo cifrado) para /tmp/src.tgz
import { writeFileSync } from "node:fs";
const repo = process.env.SOURCE_REPO || "brmaia96/lgm-engenharia";
const ref = process.env.SOURCE_REF || "main";
const res = await fetch(`https://codeload.github.com/${repo}/tar.gz/refs/heads/${ref}`);
if (!res.ok) throw new Error(`download falhou: HTTP ${res.status}`);
writeFileSync("/tmp/src.tgz", Buffer.from(await res.arrayBuffer()));
console.log(`fonte: ${repo}@${ref}`);
