# LGM Engenharia — identidade visual

Luis Gustavo Maia · Eng. Civil · CREA-SP 5071068977 · Marília-SP, atende Brasil
WhatsApp (14) 99185-0799 · engmaia1996@gmail.com · @eng.gustavomaia

## Regra

**Toda peça visual — site, apresentação, proposta, carrossel, relatório — segue a
identidade editorial abaixo.** Não há exceção por pressa ou por formato.

Referências do cliente: **SysHaus** e **Studio Arthur Casas**. Arquitetura
brasileira de alto padrão: papel, respiro, régua fina, tipografia leve.
Silêncio visual é o ponto, não ausência de esforço.

## Marca

A assinatura é **`L.`** — um L com ponto, peso leve, o ponto em terra.
Nunca em caixa-alta condensada, nunca com contorno, nunca sobre fundo colorido.
Em peça pequena, `L.` sozinho; em peça grande, `L.` com
`LGM ENGENHARIA` em micro-rótulo ao lado.

## Cor

```css
--paper:  #F6F4F0   /* fundo */
--paper2: #EFECE6   /* fundo alternado */
--ink:    #14120F   /* texto principal */
--ink2:   #55504A   /* texto secundário */
--ink3:   #8C867D   /* rótulo, legenda */
--terra:  #7A6B5A   /* acento — pedra quente */
--rule:   rgba(20,18,15,.14)   /* régua */
--rule2:  rgba(20,18,15,.07)   /* régua sutil */
```

Escuro (inversão, mesma lógica): `--paper:#0E0D0B` · `--ink:#EDEAE4` ·
`--ink2:#A8A29A` · `--ink3:#716B63` · `--terra:#A8947C`.

Terra é o **único** acento. Usar com parcimônia: um dado, uma palavra, o ponto
da marca. Nunca em bloco grande, nunca em botão preenchido.

**Proibido:** laranja ferrugem `#C8793E`, fundo preto industrial `#060605`,
gradiente, qualquer cor saturada. Essa é a linguagem dos carrosséis antigos de
Instagram e está aposentada para peça institucional.

## Tipografia

```css
--fs: 'Jost', 'Century Gothic', 'Futura', system-ui, sans-serif;  /* sistema */
--fe: 'Spectral', Georgia, serif;                                 /* editorial */
```

- **Jost** em 200/300/400/500. Display sempre em **200 ou 300** — peso leve em
  tamanho grande é a assinatura. `letter-spacing` negativo no display (−.02em).
- **Spectral 300 itálico** só para citação e nome de projeto. Com moderação.
- Micro-rótulo: 0.59rem, peso 500, `letter-spacing: .2em`, caixa-alta, `--ink3`.
- Corpo: peso 300, `line-height` 1.75 ou mais. Respiro é conteúdo.
- **Bebas Neue está proibida** em peça institucional.

## Layout

- Margem generosa. `padding` de seção em `clamp(62px, 10vw, 120px)`.
- **Régua fina separa; cartão não.** Sem `border-radius`, sem `box-shadow`,
  sem fundo em caixa. Hierarquia por espaço, peso e régua.
- Sempre alinhado à esquerda. Nunca centralizado.
- Lista de projetos como **índice tipográfico** (numeral romano, nome, local,
  dado), no espírito de sumário de monografia — não como grade de cards.
- Número grande em peso 200, com unidade em `<sup>`.
- Grade assimétrica. Coluna de texto em até ~34em.

## Texto

Tom do cliente: direto, técnico, vende pela consequência do erro, não pelo
benefício. Frases curtas. Sem emoji. Sem exclamação.

Frases da casa, usar como estão:
- "Do terreno. À chave."
- "Projeto, execução e a engenharia tributária da obra — com uma única
  responsabilidade técnica."
- "Sem terceirizar, sem delegar o que importa."

## Posicionamento

**INSS e CNO é o gancho** (ninguém no nicho fala disso; R$ 28.000 de economia
por obra chama atenção). **Projeto e execução é o motor** (é o que fatura).
Em peça institucional, projeto vem primeiro; INSS entra como o diferencial.

## Dados que podem ser citados

- 8 anos em Light Steel Frame, desde 2018 (estágio 2018–2020, formação 2020,
  construtora 2022, operação própria dez/2023, integral 2026)
- 6 projetos, 2.015 m²: Clínica Grizzo 380m² Jaú · Residência A.J. 750m² Marília
  (com CNO e averbação) · Casa Cubo 180m² · Residência Steeltec 200m² LSF ·
  Estande de Vendas 55m² em 40 dias · Barracão e Loft 450m² 100% LSF com vão
  livre acima de 10m
- LSF é cerca de 3% da construção civil brasileira

**Antes de citar norma, portaria, taxa de financiamento ou número de mercado em
peça pública: confirmar na fonte primária** (ABNT, DOU, Caixa, CBCA). O CREA
dele vai no rodapé.

## Organização de arquivo

O sistema real vive em `Desktop\LGM - Engenharia`, espelhado no Drive.
Clientes em `03. Clientes\<Código Permanente 4 dígitos>. Nome - Cidade`, com
subpastas `00. Recebidos` · `01. Projeto` · `02. Comunicações` ·
`03. Documentos` · `04. Entregas` · `05. Modelo Revit` · `06. Proposta` ·
`99. Arquivo`. O plugin pyRevit lê
`Cadastro de Clientes - Código Permanente.csv`.

Proposta gerada vai em `06. Proposta`, nomeada
`Proposta <ano-nnn> - <código>. Nome - Cidade`.
Resumo de reunião vai em `02. Comunicações`.
**Não criar estrutura paralela.** Nunca reaproveitar Código Permanente.
