#!/usr/bin/env bash
# Install Command da Vercel (projeto sem integração Git): baixa o código público,
# que inclui o acervo CRIPTOGRAFADO, e instala as dependências.
# Tudo dentro de { } para o bash ler o script inteiro antes de o cp sobrescrevê-lo.
{
  set -euo pipefail
  node deploy/fetch-source.mjs
  mkdir -p /tmp/src
  tar xzf /tmp/src.tgz -C /tmp/src --strip-components=1
  cp -a /tmp/src/acervo/. .
  rm -rf /tmp/src /tmp/src.tgz
  npm ci --no-audit --no-fund
  exit 0
}
