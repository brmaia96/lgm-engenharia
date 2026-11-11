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

## Instruções do cliente de nov/2026 (valem sobre as anteriores)

- **IA de imagem: sempre ChatGPT ou Gemini, que ele já paga.** Chave do Gemini
  (AI Studio) salva no ambiente para generativelanguage.googleapis.com, usada
  como Bearer no endereço compatível com OpenAI (`/v1beta/openai/...`). Os
  modelos de imagem (gemini-3-pro-image, 2.5/3.1-flash-image) dão 429 com
  limite 0 no plano gratuito: falta ele ativar o faturamento do projeto da
  chave no AI Studio. A assinatura do app não cobre a API.
- **Fotos das obras com acabamento realista por IA** ("falei mil vezes para
  renderizar na IA"), sobre o render fiel ao projeto, conferido depois contra
  as pranchas. Até o faturamento do Gemini estar ativo, ficam os renders.
- **Filme abre a home e começa sozinho** (mudo; o primeiro toque liga o som).
  Ele reclamou de ter de apertar reproduzir.
- **Cards coloridos** também no celular (a versão em cinza saiu).
- **Blog: imagem tem de fazer sentido com o texto.** Artigos de imposto usam
  ilustração própria (`site-build/blog-art/make.js`: ficha do CNO e 30 dias,
  linha do tempo de cinco anos, balança do ajuste, corte da parede); os de
  steel frame usam o 3D da estrutura. Texto do artigo na largura toda.

## Site (web) — direção aprovada

O cliente apontou **sys.haus** como o modelo ("é assim que eu quero"). O site
segue essa linguagem e fica em `site/` (HTML estático, pronto para hospedar).

- **Estrutura:** `index.html` (vídeo de apresentação, INSS, comparador estrutura ×
  pronta, obras em destaque, blog), `obras.html` (cartões padronizados + filtro),
  uma página por projeto `o-<slug>.html` (frase de abertura, ficha de cinco linhas
  e poucas imagens), `inss.html` (cálculo em quatro linhas, calculadora por estado
  que mostra o que a Receita cobraria e leva ao formulário de contato, mapa das
  obras aferidas, sistemas e perguntas), `sobre.html`, `agenda.html`
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

### Regra editorial: básico, direto, sem entregar o caminho (instrução do cliente, nov/2026)

Palavras dele: "você tá colocando muita coisa mastigada e não é assim. Eu quero
ser referência. Quem é referência segura conhecimento e fala o básico, pois assim
as pessoas vão querer vir. Não posso dar de mão beijada, tem que lutar para falar
comigo."

- **Texto sempre básico, direto e reto.** A página mostra que o problema existe,
  que há caminho e que ele domina o assunto. O "como" fica para a conversa. Nada
  de passo a passo, lista de documentos, lista de notas fiscais, percentuais de
  enquadramento, tabela de regras ou memória de cálculo.
- **Fonte: só o título.** Sem link e sem PDF ("isso não existe").
- **Obras: o mínimo.** Capa e no máximo quatro imagens, ficha de cinco linhas, só
  a frase de abertura, legenda só com o nome. "Não precisa de tanto detalhe."
- **Imagem de projeto tem de ser real e seguir o projeto.** O cliente reclamou do
  Le Blanc Lofts: as imagens geradas por IA que estavam na pasta dele mudavam o
  projeto (janela na fachada que não existe, interior diferente a cada vista).
  Só entra o que vem do projeto: vistas do modelo, prancha, 3D da estrutura,
  render do próprio modelo ou foto. Não gerar nem "melhorar" imagem de projeto
  por IA. Exceção declarada: Casa do Bosque, que é modelo e vai rotulada assim.
- **Todo texto corrido justificado, sempre, também na web**, com hifenização.
- A afirmação continua tendo de estar conferida na fonte primária, mesmo que a
  página só cite o título. As versões longas e conferidas ficaram guardadas em
  `site-build/arquivo/` (`blog-versao-longa.py` e `inss_page-versao-longa.py`),
  só para consulta: não voltam ao ar.

### Prioridade do site (instrução do cliente, nov/2026)

**A parte tributária é o centro.** É onde o cliente domina e o que traz o
cliente: o site tem de soar como especialista total em INSS de obra. O portfólio
só mostra que há know-how, sem excesso.

- Navegação: `inss · obras · blog · sobre · agenda`. Desde a v25 a home **abre**
  com o INSS (h1 "A obra paga INSS. Quase sempre a mais.", a frase da casa, os
  dois números e o botão da calculadora na primeira tela); o filme vem logo
  depois, dentro da coluna. Se o cliente preferir o filme no topo, é só inverter
  os dois blocos em `build.py`.
- `inss.html`, na ordem que o cliente pediu ("ficou muito maçante, muito texto;
  breve cálculo e já a calculadora; daí o mapa com as obras aferidas e um
  contador de m² e desconto; no final INSS steel frame, wood, modular; depois
  perguntas frequentes"): frase de abertura, cálculo em quatro linhas,
  calculadora, formulário de contato, mapa com contadores, três sistemas,
  perguntas curtas e fontes só pelo título. Tudo em `site-build/inss_page.py`.
- **Calculadora por estado, com os dados antes do resultado.** "O que vale é o
  estado, cada estado tem seu VAU": o visitante escolhe a UF e o VAU entra
  sozinho. Como na calculadora que o cliente já tinha (pasta `site-calculadora`
  do Drive, feita com o estudo de 351 simulações), ele se identifica e só então
  vê o valor: o que a Receita cobraria sem planejamento e o teto de redução
  ("até R$ X a menos"). O como fica para a conversa. Sequência igual à do Sero,
  conferida nas memórias reais do cliente: área equivalente (89%, duas casas
  decimais) × VAU = custo da obra; 20% de mão de obra; fator social da faixa de
  área real; 36,8%. Uma memória real (235,04 m², SP, 07/2022) fecha centavo a
  centavo com a fórmula. Só residencial unifamiliar, obra nova, pessoa física:
  comercial, multifamiliar e reforma vão para o WhatsApp.
- **VAU: `site-build/vau_uf.json`**, residencial unifamiliar, 27 UFs, novembro
  de 2026 (SP R$ 2.725,32). A tabela oficial só abre dentro do Sero (e-CAC); os
  valores vêm de consultorias que a reproduzem, e 19 pontos de memórias reais
  do Sero (SP, MT e PR, de mar/2025 a nov/2026) batem com elas centavo a
  centavo; SP residencial de novembro vem da tabela (outubro × 1,0029). **Atualizar todo mês**: sobe pela variação do Sinapi e é revisto em
  janeiro. O exemplo da home sai daí: casa de 150 m² em São Paulo, R$ 10.711
  sem planejamento (sempre calculado como alvenaria, e a página diz isso), até
  70% a menos. Os exemplos antigos (R$ 8.832, R$ 7.860,
  R$ 2.358) usavam VAU hipotético e não devem voltar.
- **Contato (base de clientes).** O cadastro pede nome, WhatsApp, e-mail, cidade
  e fase da obra, com aceite de contato e caixa opcional de avisos (a comunidade
  que ele quer formar). Hoje, ao enviar, a conversa no WhatsApp abre com tudo
  preenchido e a estimativa. Para a base gravar sozinha falta decidir com ele o
  destino e preencher `LEADS` em `inss_page.py`: Formulário Google ligado a uma
  planilha dele (`tipo='google'`) ou serviço que recebe JSON (`tipo='json'`; o
  protótipo dele usava o FormSubmit com o e-mail no endereço, o que expõe o
  e-mail no código da página e depende de ativação por e-mail: só com aprovação
  dele). Com a base ligada, o botão só mostra o resultado e o WhatsApp vira o
  segundo passo.
  Contadores e filme mostram os números arredondados (6.716 m², R$ 101.998); a
  tabela arredonda a diferença exata (Marília 2021: R$ 28.153).
  **Escolhido em nov/2026 (cliente: "pode criar"):** planilha "Base de contatos -
  site (calculadora de INSS)" criada no Drive dele, com cabeçalho; script em
  `site-build/leads_apps_script.gs` (grava a linha, corta em 200 caracteres e
  impede fórmula). O site ganhou `tipo='script'` (JSON em text/plain, sem
  checagem de CORS), testado de ponta a ponta. Falta só ele colar o script
  (Extensões > Apps Script), implantar como App da Web (executar como eu,
  acesso: qualquer pessoa) e mandar a URL /exec, que vai em `LEADS`. O link da comunidade vai em `COMUNIDADE_URL` quando existir.
- Blog (`blog.html`, artigos `b-<slug>.html`, conteúdo em `site-build/blog.py`):
  lista com imagem ("imagens chamam atenção"), um minuto de leitura por artigo:
  resposta curta, o que muda, o ponto de atenção. Primeiro os tributários;
  steel frame depois.
- **Planta (instrução do cliente, nov/2026):** "sempre que colocar planta tem que
  ser humanizada e sem medidas, no máximo medida do terreno". Nunca planta técnica,
  cotada ou com carimbo; nunca cota de ambiente. Hoje nenhuma planta está no ar.
- **Portfólio no mínimo, sem prancha.** Só fachada, externa, interna e o 3D da
  estrutura. Nada de planta, corte, isométrica, lista de corte ou detalhe:
  "detalhe é para obra e para o cliente que comprar". A seleção fica na camada
  `LEAN` de `site-build/data.py`.
- **Le Blanc Lofts**: só as vistas do modelo de arquitetura (perspectivas e
  fachadas da prancha 02) e o 3D da estrutura em steel frame. As imagens
  "ChatGPT Image" da pasta dele mostram janela na fachada que o projeto não tem
  e um interior diferente a cada vista: não usar.
- **Casa do Bosque** é modelo de casa de alto padrão (450 m²), um dos posts de
  maior resultado dele; uso autorizado. As oito imagens são geradas por IA e
  não há projeto técnico: vai rotulada como **modelo**, nunca como obra entregue
  nem "Etapa: Projeto". Só a fachada de dia (a de noite muda pedra, porta e
  piso); o cinema fica fora (a TV imita logotipo de estúdio).
- **Obras novas (nov/2026, pedido do cliente), cada imagem conferida contra o
  projeto.** Nenhuma obra fica em `HELD`. Ordem de Obras em `ORDEM` (grade
  2 · 3 · 3 · 3 · 2; destaque na home: Taquaraçu, Salas, Casa do Bosque).
  - **Casa Duo** (Marília, 119,82 m², alvenaria, projeto e processo na
    prefeitura): capa = maquete do próprio modelo; só quintal e suíte do kit, com
    recorte. A fachada do kit caiu: tem faixa de vidro no muro que o modelo não
    tem. Brise de correr não confirmado. Nunca escrever "aprovado". Pedir as
    vistas exportadas do Revit para trocar as imagens.
  - **Ampliação em steel frame** (Belo Horizonte, 11 m² de projeção, 600 kg,
    430 peças; é o antigo "Do aço à estrutura"): só renders da estrutura, que
    conferem com o modelo. Fora: a explodida (objetos soltos), o detalhe e a
    isométrica repetida. A arquitetura é de terceiros.
  - **Casa da Raia** (nome público da residência térrea de Marília, 184,60 m²,
    piscina em raia de 18 m): vistas diretas do modelo BIM, tratadas como
    desenho; recortes tiram a casca da piscina que aparece sob o muro. Sistema:
    **alvenaria com telhado sobre treliças em steel frame**, nunca "casa em steel
    frame". Arquitetura de arquiteto parceiro; o escritório fez o executivo. Não
    usar o bairro no nome nem as imagens de IA nem o kit da revisão anterior.
- **Regra de capa (instrução do cliente, nov/2026):** "as imagens de obras devem
  sempre ser renderizadas em alta resolução e todas começar com a fachada; quando
  clicar aparecem internas e modelos 3D de estrutura quando tiver; nada de
  isométrico, apenas renderizada". A obra abre com UMA fachada renderizada (capa
  única, sem par com interior); internas e estrutura ficam dentro da página.
  Fora do ar por não terem render de fachada fiel ao projeto atual (`HELD` em
  `data.py`, dados prontos): só a **Casa Duo**. A Casa da Raia voltou na v29 e
  o Le Blanc Lofts na v33, com render fiel conferido (abaixo). Os renders realistas que existem no Drive são de IA e mudam
  o projeto; os modelos (IFC 92 MB, RVT 100–330 MB) passam do limite do conector
  (10 MB). Voltam quando o cliente mandar render do modelo atual.
- **Pedidas e ainda sem capa possível (nov/2026):** obra residencial em concreto
  armado em Marília (97,19 m², projeto estrutural no TQS, obra em andamento;
  material em `scratchpad/assets/obra-concreto/`: só estrutura e fotos de alvenaria
  crua, abaixo do padrão). Entra quando houver render de fachada ou foto da obra
  pronta. Nome público nunca com nome de cliente ou empresa.
  Conferido em nov/2026 se dava para montar a fachada pelas pranchas, como em
  Garça: não dá sem interpretar. A elevação põe o portão seccional no
  alinhamento, num muro de 2,60 m; o corte AA põe o portão cerca de 1 m para
  dentro, sob cobertura de 2,70 + 0,70 m; o detalhe 3D do modelo mostra
  pergolado metálico e janela alta que a elevação não tem. Precisa da vista
  exportada do modelo. A Casa Duo, idem: a única saída do modelo é a
  volumetria aérea (não serve como capa na altura do olho).
- **Prédio comercial em Garça** (no ar desde a v28; 741,69 m², steel frame,
  projeto aprovado em 2026): as fachadas "realistas" do Drive são de IA e
  redesenham o prédio. A capa é render no Cycles (Blender, `pip install bpy` em
  Python 3.11) de um modelo montado só com as medidas da Fachada 04 da prancha
  aprovada (`site-build/render/garca_blender.py`): vidro 29,25 × 5 m em três vãos,
  painel de alumínio de 2 m, caixa-d'água, muros de divisa; sem logotipo, carros
  nem vizinhos. O mesmo caminho serve para outra obra com fachada cotada.
- **Casa da Raia** (v29): capa = render no Cycles da fachada dos fundos
  (`site-build/render/raia_blender.py`), montado com as cotas da Fachada
  Posterior e conferido em vista ortogonal contra a prancha: porta de correr
  4,39–8,96 até 2,50, porta do lavabo 10,02–10,82, janela do banho 11,93–12,73
  (1,60–2,10), janela da suíte 13,87–15,37 (1,10–2,10), cumeeira a 5,15 com 30%,
  torre da caixa-d'água até 5,85.
- **Casa Garça** (v29; é a casa que o cliente chamou pelo nome da proprietária:
  nunca usar esse nome; 135,26 m² em terreno de 200 m², alvenaria com cobertura
  metálica e telha sanduíche, projeto executivo e legal, 2025): a única imagem
  realista do Drive é de IA e foi recusada. Capa = render no Cycles
  (`site-build/render/casagarca_blender.py`) com as cotas da Fachada Norte, do
  Detalhe da Fachada, da Planta de Cobertura e do Corte A-A; conferido em vista
  ortogonal. Cores neutras, porque as pranchas não as definem. O modelo Revit
  "padrão template" ainda não foi feito: o Revit não roda aqui.
- **Le Blanc Lofts** (v33, no ar de novo): o render da v30 foi reprovado pelo
  cliente ("totalmente errado, mal feito"): medidas tiradas de imagem, eixo
  espelhado, janela e marquise que não existem. Refeito em
  `site-build/render/lofts_blender.py` só com as cotas das pranchas P01 e P02
  de arquitetura (loft 4,55 × 5,65 × 6,03 sobre base de +0,10, marquise de 0,70
  na largura toda, ala do lado da rua, P01 pivotante de madeira, J01 a J05 do
  quadro de esquadrias, piso drenante, palmeiras e agaves da locação) e
  conferido por revisor independente contra as quatro fachadas e a locação; os
  desvios que ele apontou foram corrigidos antes de publicar. **Lição: em
  Blender o eixo Y tem de apontar para o norte (Y para o sul espelha a
  fachada).** Não remontar fachada a partir de medidas tiradas de imagem.
- **Conferência independente dos renders montados (nov/2026):** Casa da Raia
  fiel. Casa Garça corrigida na v33 (casa até y 17,25, corpo a 4,00 com
  platibanda de 4,50 só na frente, caixa-d'água em y 11,05–14,30, tabeira de 0
  a 8,70, muro frontal de 2,80 de ponta a ponta). Prédio comercial corrigido na
  v33 (três vãos iguais com montantes grossos a 33,2% e 67,4%, oito módulos de
  1,20 por vão, porta dupla de 2,60, vidro sobre base de +0,40, painel liso,
  muros de divisa fora da calçada). Versões antigas guardadas como
  `*.v28.png` / `*.v29.png` em `scratchpad/assets`.
- **Acabamento por IA sobre render fiel:** testado na Raia (nov/2026) e
  reprovado: não mudou o projeto, mas borrou a borda do telhado, pôs manchas no
  muro e névoa no céu. Não repetir nas outras. só com modelo aberto local (SD 1.5 +
  ControlNet com as linhas do render travadas) e só publica se não mudar nada do
  projeto, conferido contra a prancha. Na dúvida, fica o render fiel.
- Salas comerciais: capa = foto real da fachada, recortada a partir de 56% da
  altura (acima do muro: sem céu, prédios nem cerca).
- Foto "Steel frame não é moda" na home: só a parte de cima (treliças e painéis);
  o chão da obra tinha poça, sacos e ferramentas. No filme, essa cena usa o render
  da estrutura do Chalé Acolher.
- Filme: começa sozinho e mudo; o som entra no primeiro toque, clique ou tecla na
  página (os navegadores não permitem som antes disso). Trilha nova
  (`video/musica2.py`): piano, cordas, baixo e percussão leve, -16 LUFS.
- Blog: capa no topo do artigo, fachada renderizada de uma obra, 16:9 na coluna.
- Ficha sempre com Local, Área, Sistema, Escopo, Etapa (com ano, quando o
  arquivo do projeto tem o ano; Taquaraçu não tem e fica só "Projeto"); cidade com
  vírgula ("Marília, SP"); "steel frame" no texto e "Light steel frame" só na
  linha Sistema; nunca "steel framing", "LSF" ou "off-site".
- **Chalé Analândia** usa os renders do projeto que estão no Drive (A-frame com
  volume revestido em pedra, piscina e churrasqueira). As duas imagens da casa
  branca com pergolado que estão na mesma pasta são de outro cliente e não
  entram. A versão "ultra realista por IA" foi testada com modelo aberto local
  em duas forças e **reprovada**: a IA some com a escada atrás do vidro, troca a
  esquadria e muda a churrasqueira e a cobertura do anexo. Não refazer; o
  cliente proibiu ferramenta paga e exige que a imagem siga o projeto.
- **Conferência independente das imagens (nov/2026).** Dois revisores compararam
  cada imagem no ar com planta, cortes e fachadas. O padrão: saída direta do
  modelo confere (Analândia, estruturas, renders do Acolher em fundo escuro) e
  acabamento por IA que só deu textura confere (Viver, Piedade, Tiny House);
  onde a IA redesenhou, erra. Decisões em `data.py`:
  - **Casa Taquaraçu**: a aérea e a vista com a edícula saíram (a IA mudou a
    edícula de lugar e embaralhou corrimãos). Capa em par: lado esquerdo da
    imagem 13 (casa, varanda e piscina) e o estar. A cozinha vai sem a faixa da
    porta. O comparador "estrutura × pronta" da home saiu: as duas metades não
    vinham da mesma câmera nem do mesmo modelo.
  - **Chalé Acolher**: as duas externas com IA contradiziam o projeto (vãos da
    lateral, lavanderia, caixa-d'água, cor do telhado). Entram os renders
    diretos do modelo.
  - **Chalé Piedade**: a capa antiga tinha o deck com o dobro da largura do
    quadro de áreas e plantas saindo das tábuas (erro do modelo, a refazer).
    Fica a frontal.
  - **Tiny House**: capa trocada pela frontal (na outra, a janela do banho saía
    com caixilho branco; o projeto pede preto). O loft fica sobre a cozinha e o
    banho, não sobre a sala.
  - **Casa do Bosque**: suíte e banho mostravam sacada e vista por cima das
    copas, e a fachada é térrea. Fica só o par da capa.
  - Qualquer imagem nova passa pela mesma conferência antes de ir ao ar.
- **Hospedagem pública (nov/2026):** projeto `lgm-site` criado na Vercel do
  cliente (plano gratuito), publicando a pasta `site/` deste repositório. O
  projeto `lgmengenharia` da Vercel é outro sistema dele ("Administrativo
  INSS"): não mexer. A primeira publicação falhou com `git_info_fail`, porque a
  Vercel ainda não tem acesso ao repositório no GitHub: o cliente precisa
  liberar o repositório no app da Vercel (Vercel > Settings > Git > GitHub).
  Domínio próprio (.com.br) é o único custo: cerca de R$ 40 por ano no
  Registro.br.
- **Vídeo da home** (`site-build/video/`): não é resumo do site. É um filme de
  78 s com todos os serviços e os dizeres da casa, retrato pequeno e trilha
  original (`musica.py`), em dois cortes do mesmo roteiro: 16:9 para o
  computador e 4:5 para o celular (`film.html?m`), fundo no tom do painel.
  Toca mudo quando entra na tela e para quando sai; "ativar som" e
  "reproduzir/pausar" ficam na linha da legenda. Os números do filme acompanham
  os de `inss_page.py`: se mudarem, regravar (`node cap.js w` e `node cap.js m`,
  com `fontes.css` local).
- Salas comerciais (Marília): fotos reais de obra concluída. Não citar que a
  reforma começou sem alvará; elétrica e climatização são de outro responsável.

### INSS de obra: o que foi conferido na fonte (nov/2026)

Fontes lidas: IN RFB 2.021/2021 consolidada, IN RFB 2.061/2021 (CNO), Manual do
Sero v3.0 (08/2024) e páginas da Receita no gov.br.

- COD = área equivalente × VAU. O VAU oficial só aparece no Sero (e-CAC).
- Tipo mista: paredes externas ou estrutura de madeira, metal ou pré-fabricado
  (art. 25, § 17). Mão de obra presumida de 15%, contra 20% na alvenaria.
- Pré-fabricado: redução de 70% com notas de venda e montagem de pelo menos 40%
  do COD (art. 26, § 2º). Para usar, a obra é inscrita como **alvenaria**
  (Manual do Sero, item 19.5). Não contam notas de laje, fundação, piso,
  cobertura, paredes internas, elétrica e hidráulica.
- Fator de ajuste (pessoa física): remuneração declarada de 50% da RMT (70%
  acima de 350 m²) e DCTFWeb em todos os meses: aferição sem débito (art. 33).
- Nota de prestador não é crédito no Sero; o que abate é a remuneração declarada
  com vínculo à obra. Retenção não é crédito na aferição.
- Decadência: cinco anos contados do primeiro dia do exercício seguinte; em
  aferição de 2024 estava decaído o que ocorreu até 31/12/2018.
- A norma e o manual **não citam steel frame**. O enquadramento é pelo texto
  ("estrutura de metal", "pré-fabricado por terceiros"), e isso é dito no site.
- **Obras aferidas (mapa e contadores de `inss.html`, dados em `inss_page.py`):**
  o Drive tem 70 memórias de cálculo do Sero, de 38 obras, de 2021 a 2026. Contam
  as **28 com aferição concluída** (a de Marília de 2021, 576 m², confirmada pelo
  cliente em nov/2026) e Franca, que tem certidão: **29 obras, 13 cidades**
  (Marília 17; Sinop e Água Boa, MT; Assis, Botucatu, Franca, Itupeva, Mirassol,
  Pedrinhas Paulista, Piraju, São Roque, Tupã e Vargem Grande Paulista, SP),
  **6.715,79 m² de área aferida** (433,55 m² são demolição: por isso "aferida",
  não "regularizada"). Ficam fora as dez em rascunho, entre elas as
  salas comerciais de Marília (rascunho de 09/11/2026). 
- **Desconto documentado: R$ 101.997,80 em nove obras**, com um critério só. Na tabela, antes e depois são o saldo
  na aferição final, sem o INSS recolhido ao longo da obra, e a página diz isso.
  Enquadramento, pela simulação anterior contra a aferição concluída: Marília
  2021, 576 m² (46.802,38 → 18.649,69) e Sinop 2026, 205 m² (27.026,57 →
  7.909,57). Fator de ajuste, pelo débito que a própria memória concluída apura
  antes do fator e ele zera: Marília 400 m² (29.668,63), Assis 446 m²
  (10.378,47), Marília 371 m² (7.624,20), Marília 212 m² (4.513,47), Piraju
  (1.114,39), Tupã (1.098,34) e Marília 61 m² (330,61). Não entram reduções por
  remuneração declarada (o INSS dessa folha foi pago mês a mês) nem obra sem
  valor anterior na memória. No site aparecem só antes, depois e desconto dos
  quatro maiores, sem dizer o caminho. Só cidade, área, ano e valores: nunca
  nome, CNO ou endereço.
- O "R$ 28.000 por obra" dos carrosséis antigos é conta ilustrativa, não caso real.
- Revisão independente (nov/2026): três revisores conferiram 225 afirmações contra
  as normas; nenhum erro de número, 40 ajustes de redação aplicados.
- **A confirmar com o cliente:** (1) o Provimento CG nº 17/2026 da Corregedoria
  de SP, que segundo fontes secundárias dispensou a CND para averbar construção
  nos cartórios paulistas. Por isso o site não afirma que "sem certidão o
  cartório não averba"; (2) a URL /exec do script da base de contatos e o
  link da comunidade no WhatsApp.

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
- VAU da calculadora de INSS: tabela por estado em `site-build/vau_uf.json`
  (novembro de 2026), conferida contra 13 memórias reais do Sero. No Drive há
  76 memórias e simulações do Sero, de 2021 a 2026, que servem de conferência.

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

**Vale para todo meio, a web incluída.** O cliente repetiu em nov/2026: "todo
texto que tiver no site sempre justificado e alinhado, sempre". Na web, o
parágrafo corrido vai justificado com hifenização ativa e coluna de largura
controlada, inclusive nos cartões de três e quatro colunas. Ficam à esquerda
só o que não é texto corrido (rótulo, legenda, botão, link) e, no celular, as
frases dos blocos de duas colunas, onde a linha tem menos de 28 caracteres.

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
