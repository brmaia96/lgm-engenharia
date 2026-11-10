# LGM Engenharia — identidade visual

Luis Gustavo Maia · Eng. Civil · CREA-SP 5071068977 · Marília-SP, atende Brasil
WhatsApp (14) 99185-0799 · engmaia1996@gmail.com · @eng.gustavomaia

## Regra

Toda peça visual segue a identidade abaixo. Ela **não foi inventada**: foi
extraída de `portfolio.html` e `presentation.html`, que são o material aprovado
pelo cliente. Em dúvida, abra esses arquivos — eles são a fonte, este documento
é o resumo.

Direção: **editorial e sóbria.** Referências do cliente: **SysHaus** e
**Studio Arthur Casas**. O objetivo declarado é respeito e identificação com o
público-alvo de alto padrão.

**Não é minimalismo branco clínico.** A página About do Studio Arthur Casas diz
que os ambientes não devem seguir modas, tendências ou estilos, nem buscar o
gesto dramático e espetacular. A crítica descreve estética sóbria, materiais
nobres e atenção meticulosa ao detalhe — modernismo brasileiro. O alvo é
**sobriedade com calor material**: branco puro e vazio frio erram o tom tanto
quanto estridência erra.

A paleta da SysHaus nasce de material real: alumínio reciclado sobre estrutura
de aço, madeira clara, **freijó** nos puxadores, inox nos módulos. Os tokens
abaixo já servem esse papel — `--terra` é marrom de madeira, `--ink3` tem desvio
quente de alumínio escovado, `--rust` é acento material e não dourado. Por isso
não há motivo para trocá-los: o material aprovado e a referência concordam.

### Referência medida (inspeção direta, nov/2026)

Os dois sites foram abertos e medidos no navegador. Isto é observação, não relato.

**arthurcasas.com**
- Fundo `#F8F7F3`. Texto e marca em taupe `#BCAFA6`; corpo em cinza quente. **Nunca preto.**
- Fonte própria `KMR` (grotesca neo-Helvetica), fallback Helvetica Neue.
- **Zero tracking, zero caixa-alta, zero régua, zero eyebrow.** Hierarquia por
  **negrito × regular no mesmo tamanho** (11–12px).
- Grade: marca no canto superior esquerdo, conteúdo começando a ~1/3 da largura,
  coluna esquerda vazia. Foto às vezes invade a coluna vazia.
- Legenda de projeto: uma linha sob a foto — **nome em negrito à esquerda**,
  cidade em regular à direita.
- Sobre: texto grande (~24px), peso leve, cinza, coluna larga.
- Home: painel claro com a marca centralizada + foto em duotone quente ao lado.

**sys.haus**
- **Futura Light / Book** (Jost é o clone livre). Didot itálico como acento raro.
- Navegação em **minúscula**, 14px, cinza `#A0A09F`.
- Título 28px Futura Light, cinza-grafite `#2F2E2E`.
- Corpo cinza, coluna estreita, **destaque em negrito dentro da frase**.
- Espaço vertical enorme entre blocos. Foto e citação em par assimétrico.
- Rodapé: blocos com rótulo em negrito e texto regular.

**Consequência para a web:** a peça web segue esse vocabulário — Jost, texto em
cinza quente, rótulo em negrito 12px sem tracking, navegação minúscula, coluna
de conteúdo a 1/3, legenda nome × cidade, foto em duotone quente, nenhuma régua.
O eyebrow de 7px com tracking .32em e a régua de 32px vêm do `portfolio.html`
antigo e **não existem nas referências** — não usar em peça nova.

Implementação de referência: o site publicado (`site-lgm.html`), tokens
`--ink #3A3632`, `--body #6B655E`, `--quiet #A39A90`, `--tone #E6E0D7`,
`--paper #F6F4F0`, `--rust #C9703A` só no numeral de destaque.

Instagram (`@eng.gustavomaia`) passa pela rede, mas exige login — não é
acessível sem conta. Para referência dos posts, pedir print ao cliente.

## Site (web) — direção aprovada

O cliente apontou **sys.haus** como o modelo ("é assim que eu quero"). O site
segue essa linguagem e fica em `site/` (HTML estático, pronto para hospedar).

- **Estrutura:** `index.html` (vídeo de apresentação, comparador estrutura ×
  pronta, obras em destaque, INSS), `obras.html` (cartões padronizados + filtro),
  uma página por projeto `o-<slug>.html` (texto curto, ficha técnica, galeria por
  seção com ampliação), `inss.html` (exemplo, memória de cálculo, simulador que
  mostra só a aferição indireta e leva ao WhatsApp), `sobre.html`, `agenda.html`
  (escolha de dia e horário; o botão principal cria o evento no Google Agenda
  do visitante com o engenheiro como convidado, uso do e-mail autorizado pelo
  cliente; o WhatsApp é a segunda opção. Quando existir a página de
  agendamento do Google Agenda, preencher `AGENDA_URL` em
  `site-build/static_pages.py`).
- **Tokens web:** fundo `#fff`, tinta `#2F2E2E`, corpo `#6B6868`, apoio `#A0A09F`,
  linha `#E9E8E6`, acento terra `#9A7350` só em destaque raro. Jost 300/400/500;
  Playfair Display só na marca e em um itálico de acento.
- **Marca na web:** `L` em serifa didone com o ponto cobre `#C89A71`, como no
  perfil e nos vídeos publicados pelo cliente. (A regra "monocromática" abaixo
  vale para a peça A4 impressa.)
- **Nunca nome de cliente.** Cidade pode. Nome de projeto pode ser trocado.

### Padrão de imagem (obrigatório em toda peça web)

Toda imagem pertence a uma de três famílias, cada uma com um só tratamento:

1. **Render ou foto** — cor graduada única: branco neutro-quente, saturação
   contida (~60%), exposição nivelada. Nada de pôr do sol laranja ao lado de céu
   azul saturado.
2. **Desenho técnico** — uma tinta só (`#2F2D2B`) sobre o mesmo papel
   (`#F7F6F4`). Cotas e hachuras coloridas viram cinza.
3. **Modelo de estrutura em fundo escuro** — monocromático sobre o mesmo preto
   (`#0A0A0A`).

Capas (Obras e home) em duotone tinta × papel; a cor aparece só no hover.
Proporções fixas: 3:2 imagem inteira, 4:3 pares, 1:1 trios, 4:5 planta vertical.
Ordem fixa por projeto: capa, fachadas, interiores, planta, estrutura.
Retrato do engenheiro: preto e branco, fundo de estúdio liso, sem logos.

Para render novo sair já no padrão: mesma hora do dia, câmera na altura do olho
em três quartos para a capa, e o conjunto capa + 2 fachadas + 3 internas +
planta sem cotas + estrutura.

### Fatos conferidos no Drive (nov/2026)

- Papanduva é **cobertura metálica de pátio escolar** (784 m², 20,2 t), não
  steel frame.
- Chalé Viver é **alvenaria com concreto armado**; Chalé Acolher é steel frame.
- Todas as imagens de projeto são renders; nenhuma obra executada documentada.
  Ficha usa "Etapa: Projeto".
- A cobertura de estacionamento de Recife ficou **fora** do site até o cliente
  confirmar que pode ser publicada.
- VAU do simulador de INSS: referência de R$ 2.000/m² (o oficial só no e-CAC).

## Tokens da peça A4 (exatos, de portfolio.html)

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

**Distinguir o meio.** Em peça A4 impressa — proposta, portfólio, apresentação —
justificar é a convenção de monografia e está certo. Em web, o padrão de site de
estúdio de arquitetura é coluna estreita alinhada à esquerda, porque o navegador
hifeniza pior e a largura varia com a janela. Justificar na tela só com coluna
de largura controlada e hifenização ativa; em dúvida na web, esquerda.

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

## A marca é `L.`

**A marca é o lettermark `L.` — um L seguido de ponto.** Instrução direta e
repetida do cliente.

**O `LGM` tipografado que aparece em `portfolio.html` e `presentation.html`
não é a marca.** Aqueles arquivos são a fonte da paleta e das medidas, não da
marca. `LGM` não tem relação com `L.` — não substituir um pelo outro, não
alternar entre os dois, não usar `LGM` como marca em peça nova.

Aplicação:

```css
font-family: var(--D);
font-weight: 200;
letter-spacing: -.025em;   /* dois glifos: tracking amplo solta o ponto */
line-height: .9;
```

- Peça A4: 88px na tela, 42mm em print. Marca d'água: 300px / 170mm,
  opacidade .05.
- **Monocromática.** O ponto é da mesma cor da letra. Não colorir o ponto,
  não usar terra nem rust na marca — minimalismo não decora.
- Tracking **negativo**. O tracking amplo de .14em era para a palavra `LGM`;
  em dois glifos ele desgruda o ponto do L e quebra a marca.
- Onde o nome por extenso é necessário (rodapé de documento técnico, registro
  profissional), usar **Luis Gustavo Maia · CREA–SP 5071068977** — é em nome
  dele que a ART é registrada.

Ainda não fornecido pelo cliente: arquivo SVG, área de respiro formal, tamanho
mínimo e versão reversa. Se ele enviar, registrar aqui.

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
