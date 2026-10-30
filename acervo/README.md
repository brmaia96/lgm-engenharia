# Cobogó — Acervo de Arquitetura

Site privado (login de 2 usuários) com a base de projetos de arquitetura: filtros, ficha técnica,
e para cada projeto **fachadas, internas, planta baixa e layout**, com visualizador em tela cheia.

## Como funciona a proteção de dados

| Camada | O que faz |
|---|---|
| **Acervo cifrado** | Catálogo e imagens ficam em `vault/` cifrados com AES‑256‑GCM. O repositório (público) só tem bytes ilegíveis com nomes aleatórios. A chave existe apenas na variável `VAULT_KEY` do servidor. |
| **Login** | Senhas guardadas só como hash scrypt em `AUTH_USERS`. Sessão em cookie `httpOnly` assinado (12 h). Limite de 6 tentativas / 15 min por IP. |
| **Duas barreiras** | O `proxy.ts` bloqueia tudo sem sessão, e a rota de imagens confere a sessão de novo antes de decifrar. |
| **Sem nomes de clientes** | Projetos têm só código (`CB014`) e nome padronizado. Metadados EXIF/GPS das fotos são apagados na entrada. |
| **Invisível para buscadores** | `noindex` em cabeçalho, meta e `robots.txt`; CSP restritiva; sem iframe. |

## Padrão de nome

```
ARQ_R_15X20_T_150M2_3SUITES        código curto: CB001, CB002…
│   │ │     │ │     └ suítes (ND = a confirmar)
│   │ │     │ └ área construída (ND = a confirmar)
│   │ │     └ pavimentos: T térreo · TM térreo+mezanino · S sobrado · 3P · SS subsolo
│   │ └ terreno frente×fundo (ND = a confirmar)
│   └ tipo: R residencial · H hospedagem/chalé · C comercial · I institucional · M misto
└ arquitetura
```

O site tem um gerador interativo na aba **Padrão**.

## Incluir um projeto novo

```
incoming/casa-nova/
├── projeto.json          ← copie de docs/projeto.exemplo.json
├── fachada/  capa.jpg 01.jpg …
├── interna/  sala.jpg cozinha.jpg …
├── planta/   planta-baixa.pdf      (PDF vira imagem; corte o carimbo antes!)
└── layout/   humanizada.png
```

```bash
npm run acervo:add -- incoming/casa-nova --dry   # confere sem gravar
npm run acervo:add -- incoming/casa-nova         # otimiza, cifra, gera CB0xx
git add vault && git commit -m "acervo: CB0xx" && git push
```

Outros comandos: `acervo:list`, `acervo:edit -- CB004 area=162 suites=3 terreno=12x30`,
`acervo:remove -- CB004`, `acervo:export` (backup decifrado em `export/`, fora do git).

Para tudo isso o arquivo `acervo/.env` precisa ter a mesma `VAULT_KEY` do servidor (veja `.env.example`).

## Usuários

```bash
npm run acervo:user -- rafael     # pede a senha e imprime a linha do hash
```
Junte as linhas com `;` na variável `AUTH_USERS` do servidor e reimplante. Remover a linha corta o acesso na hora.

## Hospedagem

- **Vercel** (atual): variáveis `VAULT_KEY`, `AUTH_SECRET`, `AUTH_USERS`. Sem integração Git, o
  install command `bash deploy/bootstrap.sh` baixa este código do GitHub (`SOURCE_REF` = branch).
- **Render**: `render.yaml` na raiz do repositório (Blueprint), mesmas variáveis.

## Desenvolvimento

```bash
cp .env.example .env   # preencha
npm install
npm run dev
```
