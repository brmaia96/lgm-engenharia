#!/usr/bin/env bash
# Usado como "Install Command" na Vercel quando o projeto é implantado sem integração Git:
# baixa o código (público, com o acervo CRIPTOGRAFADO) do GitHub e instala as dependências.
set -euo pipefail
REPO="${SOURCE_REPO:-brmaia96/lgm-engenharia}"
REF="${SOURCE_REF:-main}"
node -e 'fetch(process.argv[1]).then(r=>{if(!r.ok)throw new Error("HTTP "+r.status);return r.arrayBuffer()}).then(b=>require("fs").writeFileSync("/tmp/src.tgz",Buffer.from(b)))' "https://codeload.github.com/${REPO}/tar.gz/refs/heads/${REF}"
mkdir -p /tmp/src && tar xzf /tmp/src.tgz -C /tmp/src --strip-components=1
cp -a /tmp/src/acervo/. .
rm -rf /tmp/src /tmp/src.tgz
npm ci --no-audit --no-fund
echo "acervo: $(ls vault/media 2>/dev/null | wc -l) arquivos cifrados em vault/media"
