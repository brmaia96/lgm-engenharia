# LGM Engenharia — identidade visual

Luis Gustavo Maia · Eng. Civil · CREA-SP 5071068977 · Marília-SP, atende Brasil
WhatsApp (14) 99185-0799 · engmaia1996@gmail.com · @eng.gustavomaia

## Regra

Toda peça visual segue a identidade abaixo. Ela **não foi inventada**: foi
extraída de `portfolio.html` e `presentation.html`, que são o material aprovado
pelo cliente. Em dúvida, abra esses arquivos — eles são a fonte, este documento
é o resumo.

Direção: **minimalista e editorial.** Referências do cliente: **SysHaus** e
**Studio Arthur Casas**. O objetivo declarado é respeito e identificação com o
público-alvo de alto padrão — silêncio visual, não estridência.

## Tokens (exatos, de portfolio.html)

```css
--ink:   #0D0D0D;   /* texto principal */
--ink2:  #3A3A3A;   /* texto secundário */
--ink3:  #888880;   /* rótulo, legenda */
--paper: #F6F4F0;   /* fundo da página */
--p2:    #ECEAE5;   /* fundo alternado */
--terra: #7A6B5A;   /* rótulo, eyebrow, régua de acento */
--rust:  #C9703A;   /* numeral de destaque — só número */
--line:  rgba(13,13,13,.10);
--D: 'Gill Sans MT','Gill Sans','Century Gothic',Calibri,sans-serif;  /* display */
--B: 'Segoe UI',system-ui,-apple-system,Arial,sans-serif;             /* corpo */
```

Fundo do envelope (fora da página, na tela): `#E8E6E2`.

**Dois acentos, com função separada:** terra em rótulo e régua; rust **apenas em
numeral de destaque** (valor de pilar, número de etapa, paginação). Nunca rust em
bloco, botão ou texto corrido.

Em web, onde Gill Sans e Century Gothic não existem, carregar **Jost** do Google
Fonts como fallback — colocar **depois** das faces nomeadas, nunca no lugar delas.

## Tipografia — medidas que são a assinatura

- **Eyebrow: 7–8px**, `letter-spacing` .22em a .32em, caixa-alta, cor terra.
  Minúsculo e muito espaçado. É o detalhe que identifica a marca.
- **Display em peso 200 ou 300.** Nunca negrito. Numeral grande em 200.
- Título de página: 19–22px, peso 300, `letter-spacing` −.01em.
- Numeral de destaque: 26–28px, peso 200.
- Subtítulo em itálico: 13px, peso 300.
- Corpo: 9–13px na página A4.

Escala pequena é proposital: a peça é A4, não tela grande.

### Texto corrido é sempre justificado

Instrução direta do cliente: **sempre justificar, sempre alinhar.** É a
convenção de monografia e revista de arquitetura — e é o que separa a peça
editorial do post de rede social.

```css
text-align: justify;
text-justify: inter-word;
hyphens: auto;          /* junto de -webkit-hyphens: auto */
```

A hifenização não é opcional: sem ela, justificar em português abre rios de
espaço entre palavras e o efeito se inverte. Exige `lang="pt-BR"` no elemento
que envolve o texto, ou o navegador não sabe onde hifenizar.

Justifica-se **texto corrido**. Rótulo, eyebrow, numeral, valor em coluna e
título continuam alinhados à esquerda (ou à direita, quando em coluna de
valores). Coluna de texto justificado precisa de largura mínima razoável —
abaixo de ~28 caracteres, justificar piora.

### Alinhamento

Tudo assenta na mesma grade. Valor em coluna usa `grid`, não `flex-wrap`, para
que as colunas fiquem alinhadas de fato. Rótulo e valor compartilham a mesma
borda esquerda em todas as linhas. Nada centralizado.

## Layout

- **Print-first.** Sistema de página: `.page` 390×693px na tela, **A4 retrato na
  impressão** (`@page { size: A4 portrait; margin: 0 }`), com
  `page-break-after: always`. Toda peça institucional nasce para virar PDF.
- Margem interna em print: **8mm** nas laterais.
- **Régua é um tique curto de 32px × 1px**, não linha de ponta a ponta.
  `.rule-terra` quando precisa de acento.
- **Fotografia é protagonista.** Containers `.photo` com placeholder e altura
  fixa: projeto 145mm, grade 72mm, sobre 50mm, capa full-bleed 210×297mm.
  `object-fit: cover`. O placeholder desaparece sozinho com
  `.photo:has(img) .photo-placeholder { display:none }`.
  **Não substituir foto por tipografia** — o sistema foi feito para a foto.
- Paginação discreta: `.pg-badge` no topo direito, 8px, opacidade baixa.
- Alinhado à esquerda. Sem `border-radius`, sem sombra.

## Texto

Direto, técnico, vende pela consequência do erro. Frases curtas. Sem emoji,
sem exclamação.

Frases da casa:
- "Do terreno. À chave."
- "Projeto, execução e a engenharia tributária da obra — com uma única
  responsabilidade técnica."
- "Sem terceirizar, sem delegar o que importa."
- "Steel frame não é moda. É engenharia."

## Posicionamento

**INSS e CNO é o gancho** — nenhum concorrente de Instagram fala disso, e
R$ 28.000 de economia por obra para o scroll. **Projeto e execução é o motor** —
é o que fatura. Em peça institucional, projeto primeiro; INSS como diferencial.

## Dados citáveis

- 8 anos em Light Steel Frame, desde 2018 (estágio 2018–2020, formação 2020,
  administradora de obra 2020, construtora 2022, operação própria dez/2023,
  dedicação integral 2026)
- 6 projetos, 2.015 m²: Clínica Grizzo 380 m² Jaú · Residência A.J. 750 m²
  Marília (com CNO e averbação) · Casa Cubo 180 m² · Residência Steeltec
  200 m² LSF · Estande de Vendas 55 m² em 40 dias · Barracão e Loft 450 m²
  100% LSF com vão livre acima de 10 m
- LSF é cerca de 3% da construção civil brasileira

**Credenciais a acertar:** `presentation.html` diz "8+ anos / 120+ projetos",
`portfolio.html` diz "7+ anos / 85+ unidades". Usar a trajetória acima, que é
verificável, até o cliente definir o número.

**Antes de citar norma, portaria, taxa de financiamento ou dado de mercado em
peça pública: confirmar na fonte primária** (ABNT, DOU, Caixa, CBCA). O CREA
dele vai no rodapé.

## A LOGO NÃO ESTÁ DEFINIDA AQUI

O cliente confirmou que **a logo usada nos arquivos deste repositório está
errada** — o `LGM` tipografado em 72px de `portfolio.html` e
`presentation.html` não é a marca atual.

**Não desenhar, não deduzir e não reaproveitar o `LGM` tipografado.** Logo é a
única coisa que não se infere. Enquanto o cliente não fornecer o arquivo (SVG
de preferência) ou a especificação, deixar um espaço reservado nomeado e
perguntar.

Quando a marca chegar, registrar aqui: arquivo, área de respiro, tamanho
mínimo, versão reversa e usos indevidos.

## Pendência conhecida

As **20 imagens** referenciadas (`p1_01.png` a `p6_04.png`, `obra.svg`,
`casa.svg`) e o retrato não estão no repositório — `portfolio.html` e
`presentation.html` renderizam com placeholder no lugar. Conseguir essas fotos é
pré-requisito para qualquer peça pública.

## Organização de arquivo

Sistema real em `Desktop\LGM - Engenharia`, espelhado no Drive.
Clientes em `03. Clientes\<Código Permanente 4 dígitos>. Nome - Cidade`, com
subpastas `00. Recebidos` · `01. Projeto` · `02. Comunicações` ·
`03. Documentos` · `04. Entregas` · `05. Modelo Revit` · `06. Proposta` ·
`99. Arquivo`. O plugin pyRevit lê
`Cadastro de Clientes - Código Permanente.csv`.

Proposta gerada vai em `06. Proposta`, nomeada
`Proposta <ano-nnn> - <código>. Nome - Cidade`.
Resumo de reunião vai em `02. Comunicações`.
**Não criar estrutura paralela.** Nunca reaproveitar Código Permanente.
