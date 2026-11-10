import importlib.util,os
_s=importlib.util.spec_from_file_location('sp',os.path.dirname(__file__)+'/static_pages.py'); _m=importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
INSS_BODY=_m.INSS_BODY; SOBRE_BODY=_m.SOBRE_BODY; AGENDA_BODY=_m.agenda_body()
OBRAS_META='11 projetos · casas, chalés e estruturas em aço'
HOME_SELECT=['casa-taquaracu','chale-piedade','patio-escolar']
CMP_CAPTION='<b><a href="o-chale-acolher.html">Chalé Acolher</a></b><span>arraste para ver a estrutura</span>'
C='clean/'
def I(src,cap,alt,lay='half',**k): d=dict(src=C+src,cap=cap,alt=alt,lay=lay); d.update(k); return d

PROJECTS=[
dict(slug='casa-taquaracu',assets='taquaracu',name='Casa Taquaraçu',cat='casa',cat_label='casas',cat_plural='casas',city='Taquaraçu de Minas · MG',sub='light steel frame · 296 m²',
 card=dict(src=C+'01-capa-aerea.jpg',focus=(.45,.6),alt='Vista aérea da Casa Taquaraçu, com piscina entre a casa e a edícula'),
 hero=dict(src=C+'01-capa-aerea.jpg',pos='50% 62%',alt='Vista aérea da casa e da edícula, com a piscina entre os dois blocos e a serra ao fundo'),
 lead='Casa e edícula em steel frame <b>numa encosta da serra mineira.</b>',
 text=['A edícula fica 1,35 m abaixo da casa. A varanda avança sobre o desnível e, entre os dois blocos, uma piscina de 27 m² ocupa o terraço.',
       'Por dentro, estar, jantar e cozinha formam um só ambiente de 86,90 m² sob a inclinação do telhado, coberto com telha sanduíche.',
       'O trabalho foi o projeto executivo, os complementares e a compatibilização de tudo com a estrutura: <b>11 modelos conversando entre si antes de a obra começar.</b>'],
 ficha=[('Local','Taquaraçu de Minas · MG'),('Área construída','296,35 m²'),('Casa e edícula','198,72 m² + 97,63 m²'),('Terreno','1.463 m²'),('Sistema','Light steel frame'),
        ('Fundação','Radier sobre pilares'),('Cobertura','Telha sanduíche, aço pré-pintado e núcleo de PU'),('Complementares','Elétrico, hidrossanitário, pluvial, piscina e ar-condicionado'),
        ('Escopo','Projeto executivo, complementares e compatibilização'),('Etapa','Projeto')],
 sections=[
  dict(label='Fachadas',items=[
   I('03-casa-piscina-e-edicula.jpg',('Casa, piscina e edícula','a edícula fica 1,35 m abaixo da casa'),'Vista do jardim para a piscina, com a casa sobre o desnível e a edícula à direita','full',pos='50% 42%'),
   I('06-varanda-e-area-gourmet.jpg',('Varanda e área gourmet','41,40 m² · vista para a serra'),'Varanda com guarda-corpo metálico e a edícula com área gourmet'),
   I('13-ficha.jpg',('Terraço da piscina','27 m² entre a casa e a edícula'),'Piscina com espreguiçadeiras entre a casa e a edícula, ao pôr do sol',pos='40% 50%')]),
  dict(label='Interiores',items=[
   I('04-estar-e-jantar.jpg',('Estar e jantar','66,55 m² sob o telhado'),'Estar e jantar integrados com forro inclinado'),
   I('05-cozinha.jpg',('Cozinha com ilha','20,35 m² · integrada ao estar'),'Cozinha com ilha e quatro banquetas')]),
  dict(label='Planta',items=[I('07-planta-baixa.jpg',('Planta baixa','casa acima, edícula abaixo'),'Planta baixa da casa e da edícula, sem cotas','plan')]),
  dict(label='Estrutura',items=[
   I('08-fundacao-e-estrutura.jpg',('Fundação e estrutura','radier sobre pilares · light steel frame'),'Modelo 3D da estrutura em steel frame sobre laje apoiada em pilares'),
   I('10-steel-frame-por-dentro.jpg',('Steel frame por dentro','montantes, painéis e treliças de cobertura'),'Vista interna do modelo da estrutura em steel frame'),
   I('11-estrutura-e-instalacoes.jpg',('Estrutura e instalações','11 modelos compatibilizados'),'Painéis de steel frame com as instalações sobrepostas em cores'),
   I('12-telha-sanduiche.jpg',('Telha sanduíche','aço pré-pintado · núcleo de PU'),'Detalhe em corte da telha sanduíche trapezoidal')])]),

dict(slug='chale-acolher',name='Chalé Acolher',cat='chalé',cat_label='chalés',cat_plural='chalés',city='Marília · SP',sub='light steel frame · 81 m²',ref='o Chalé Acolher',
 card=dict(src=C+'00-fachada-frontal-pergolado.jpg',focus=(.5,.55),alt='Fachada do Chalé Acolher, em telha metálica creme, com garagem sob pergolado'),
 hero=dict(src=C+'00-fachada-frontal-pergolado.jpg',pos='50% 58%',alt='Fachada frontal do chalé, com paredes e cobertura em telha metálica creme'),
 lead='Chalé térreo com <b>a mesma telha metálica creme nas paredes e no telhado.</b>',
 text=['A sala junta estar, jantar e cozinha em 33,54 m² e abre para os fundos por uma porta de correr de 3,00 m. Suíte com closet, um dormitório que também é escritório e lavanderia externa junto à divisa.',
       'A estrutura é em light steel frame painelizado, com <b>um só perfil em toda a obra:</b> paredes em módulo de 0,40 m, tesouras alinhadas aos montantes e laje técnica em vigas treliçadas.'],
 ficha=[('Local','Marília · SP'),('Área construída','80,57 m²'),('Projeção','7,10 × 10,65 m'),('Sistema','Light steel frame painelizado'),('Perfil','ME 90 #0,95, único em toda a estrutura'),
        ('Módulo','Montantes a cada 0,40 m'),('Fechamento','Telha metálica trapezoidal RT 45 em parede e cobertura'),('Vento de projeto','V0 = 40 m/s, categoria III'),
        ('Escopo','Arquitetura, estrutural em steel frame, complementares e caderno de montagem'),('Etapa','Projeto · 2026')],
 sections=[
  dict(label='Fachadas',items=[
   I('01-fundos-porta-de-correr.jpg',('Fundos','porta de correr de 3,00 m'),'Fundos do chalé, com a porta de correr da sala'),
   I('04-render-lateral-direita-lavanderia.jpg',('Lateral','volume da lavanderia externa'),'Lateral direita do chalé com o volume da lavanderia',pos='45% 50%')]),
  dict(label='Interiores',items=[
   I('14-a3-interna-estar.jpg',('Estar','sala integrada de 33,54 m²'),'Estar visto da cozinha, com a ilha em primeiro plano','full'),
   I('15-a3-interna-cozinha-jantar.jpg',('Cozinha e jantar','ilha com cooktop'),'Cozinha e jantar com mesa de madeira para seis lugares'),
   I('16-a3-interna-suite.jpg',('Suíte','9,15 m² · porta de correr para o gramado'),'Suíte com cama de casal e porta de correr de vidro'),
   I('18-a3-interna-dormitorio-escritorio.jpg',('Dormitório e escritório','7,80 m²'),'Dormitório com bancada de parede a parede'),
   I('24-a3-interna-banho-social.jpg',('Banho social','3,12 m²'),'Banho social com bancada escura e cuba embutida')]),
  dict(label='Layout',items=[
   I('05-render-interior-corte-layout.jpg',('Chalé em corte','layout interno com os painéis à vista'),'Chalé cortado mostrando o layout interno','full'),
   I('26-a3-isometrica-chale-aberto.jpg',('Isométrica','corte a 2,40 m do piso'),'Isométrica do chalé cortado, com a lavanderia externa','plan')]),
  dict(label='Estrutura',items=[
   I('06-render-estrutura-lsf.jpg',('Estrutura em light steel frame','painéis de parede, tesouras e cobertura'),'Estrutura completa em light steel frame','full'),
   I('08-lsf-3d-frente.jpg',('Modelo estrutural','paredes em módulo de 0,40 m'),'Vista 3D do modelo estrutural pela frente','plan half'),
   I('10-lsf-3d-sem-cobertura.jpg',('Tesouras e laje técnica','tesouras Pratt alinhadas aos montantes'),'Vista 3D do modelo estrutural sem os painéis de cobertura','plan half')])]),

dict(slug='chale-piedade',name='Chalé Piedade',cat='chalé',cat_label='chalés',cat_plural='chalés',city='Piedade · SP',sub='A-frame · 70 m²',ref='o Chalé Piedade',
 card=dict(src=C+'02-fachada-nordeste-hall.jpg',focus=(.5,.5),alt='Chalé A-frame com cobertura grafite e hall em ripado de madeira'),
 hero=dict(src=C+'02-fachada-nordeste-hall.jpg',pos='50% 55%',alt='Chalé A-frame na golden hour, com cobertura de junta elevada grafite e hall em ripado'),
 lead='Chalé A-frame de serra, <b>com a empena norte inteira em vidro.</b>',
 text=['Um triângulo de 62° sobre embasamento de concreto. A sala tem pé-direito duplo, lareira suspensa e escada caracol até o mezanino, onde fica o quarto.',
       'A cobertura é em telha metálica de junta elevada, com juntas a cada 45 cm. A empena sul e o hall de entrada são em ripado de madeira.'],
 ficha=[('Local','Piedade · SP'),('Área','70,35 m²'),('Projeção','6,40 × 9,05 m'),('Forma','A-frame a 62°'),('Níveis','Térreo e mezanino a +2,65 m'),
        ('Cobertura','Telha metálica de junta elevada'),('Mezanino','Laje em light steel frame'),('Embasamento','Concreto aparente, 1,05 m'),('Escopo','Projeto de arquitetura'),('Etapa','Projeto')],
 sections=[
  dict(label='Fachadas',items=[
   I('01-fachada-norte-hora-azul.jpg',('Empena norte','vidro de ponta a ponta, voltado para o deck'),'Empena de vidro na hora azul, com o interior aceso','full'),
   I('03-aerea.jpg',('Implantação','deck de 22,89 m² com ofurô'),'Vista aérea do chalé com o deck e o ofurô','full')]),
  dict(label='Interiores',items=[
   I('04-interna-pe-direito-duplo.jpg',('Sala','pé-direito duplo, mezanino e escada caracol'),'Sala com pé-direito duplo e mezanino com guarda-corpo de vidro','full'),
   I('05-interna-cozinha-jantar.jpg',('Cozinha e jantar','11,69 m² sob o mezanino'),'Cozinha e mesa de jantar sob o mezanino'),
   I('06-interna-mezanino-para-vidro.jpg',('Mezanino','quarto de 14,61 m² voltado para o vidro'),'Vista do mezanino para a empena triangular de vidro'),
   I('07-interna-lareira.jpg',('Lareira suspensa','no centro da sala'),'Lareira suspensa preta com fogo aceso'),
   I('08-interna-banheiro.jpg',('Banheiro','3,05 m²'),'Banheiro com paredes em tom cimento e cuba de apoio')]),
  dict(label='Planta',items=[
   I('09-planta-p1-terreo.jpg',('Térreo','sala, cozinha, banheiro, hall e deck'),'Planta humanizada do térreo','half',r='4/5'),
   I('10-planta-p2-mezanino.jpg',('Mezanino','quarto sobre a cozinha'),'Planta humanizada do mezanino','half',r='4/5')])]),

dict(slug='casa-duo',name='Casa Duo',cat='casa',cat_label='casas',cat_plural='casas',city='Marília · SP',sub='casa térrea · 120 m²',ref='a Casa Duo',
 card=dict(src=C+'01-fachada.jpg',focus=(.5,.55),alt='Fachada da Casa Duo vista da rua'),
 hero=dict(src=C+'01-fachada.jpg',pos='50% 52%',alt='Fachada da casa térrea vista da rua, com portão de garagem escuro e jardim na frente do muro'),
 lead='Dois lotes somando 320 m² <b>viraram uma casa térrea com piscina.</b>',
 text=['Três dormitórios, sendo uma suíte. Estar, jantar e cozinha integrados em 48,50 m², garagem para dois carros e piscina de 12,50 m².',
       'Na frente, o muro ganha uma faixa de vidro discreta. Entre a garagem e a piscina, um brise de correr em madeira fecha ou abre a passagem.',
       'O trabalho foi o projeto e o processo na prefeitura, <b>da unificação dos lotes ao protocolo.</b>'],
 ficha=[('Local','Marília · SP'),('Área construída','119,82 m²'),('Terreno','320 m², em dois lotes de 8 × 20 m'),('Programa','Três dormitórios, uma suíte'),('Social','48,50 m² integrados'),
        ('Telheiros','58,42 m²'),('Piscina','12,50 m²'),('Escopo','Projeto e processo na prefeitura'),('Etapa','Projeto protocolado')],
 sections=[
  dict(label='Fachadas',items=[
   I('02-aerea-dois-lotes.jpg',('Os dois lotes','320 m² · garagem para dois carros'),'Vista aérea da casa ocupando os dois lotes'),
   I('03-piscina.jpg',('Piscina','12,50 m² · brise de correr em madeira'),'Piscina com espreguiçadeiras e o brise de madeira ao fundo'),
   I('08-piscina-brise.jpg',('Quintal','jardim vertical e espreguiçadeiras'),'Piscina vista no comprimento, com jardim vertical','full',pos='50% 60%')]),
  dict(label='Interiores',items=[
   I('09-estar-jantar.jpg',('Estar e jantar','48,50 m² integrados à cozinha'),'Estar e jantar integrados, com portas de correr para o quintal','third'),
   I('04-cozinha.jpg',('Cozinha','armários sob medida e balcão'),'Cozinha com balcão e banquetas','third'),
   I('05-suite.jpg',('Suíte','15,75 m²'),'Suíte com painel ripado em madeira','third')]),
  dict(label='Planta',items=[I('06-planta-baixa.jpg',('Planta baixa','a casa no terreno'),'Planta humanizada da casa no terreno, com piscina e garagem','plan')])]),

dict(slug='tiny-house',name='Tiny House',cat='chalé',cat_label='chalés',cat_plural='chalés',city='Sorocaba · SP',sub='duas águas · 39 m²',ref='a Tiny House',
 card=dict(src=C+'02-fachada-lateral-monolito.jpg',focus=(.5,.5),alt='Tiny house em telha metálica grafite, com frente de vidro e deck'),
 hero=dict(src=C+'02-fachada-lateral-monolito.jpg',pos='50% 55%',alt='Volume de telha metálica grafite contínua em parede e cobertura, com frente de vidro'),
 lead='39 m² em duas águas, <b>com a telha dobrando da cobertura para a parede.</b>',
 text=['Uma casca de telha metálica de junta elevada, sem beiral, emoldurada por um portal preto. A frente é toda de vidro e abre para o deck.',
       'No térreo ficam sala, cozinha e banho. O loft de dormir fica sobre a sala, com uma claraboia em cima da cama e acesso por escada de degraus alternados.'],
 ficha=[('Local','Sorocaba · SP'),('Área','38,57 m²'),('Projeção','4,00 × 7,50 m'),('Forma','Duas águas a 53°'),('Níveis','Térreo e loft a +2,60 m'),
        ('Fechamento','Telha metálica de junta elevada em parede e cobertura'),('Frente','Porta de correr de vidro, 3,70 × 2,40 m'),('Deck','4,00 × 2,00 m'),('Escopo','Projeto de arquitetura'),('Etapa','Projeto')],
 sections=[
  dict(label='Fachadas',items=[
   I('01-fachada-frontal-hora-azul.jpg',('Frente','vidro de ponta a ponta, emoldurado pelo portal'),'Frente de vidro na hora azul, com o interior aceso','full'),
   I('03-aerea.jpg',('Cobertura','claraboia sobre a cama'),'Vista aérea com o deck e a claraboia'),
   I('07-fachada-fundo-ripado-noturna.jpg',('Fundo','oitão em ripado de madeira'),'Oitão posterior em ripado iluminado à noite')]),
  dict(label='Interiores',items=[
   I('04-interna-sala-para-vidro.jpg',('Sala','9,73 m² voltados para o vidro'),'Interior voltado para a frente de vidro','full'),
   I('05-interna-loft.jpg',('Loft','14,65 m² · cama sob a claraboia'),'Loft com a cama sob a claraboia'),
   I('06-interna-cozinha-escada.jpg',('Cozinha e escada','degraus alternados'),'Cozinha em L e escada de degraus alternados')]),
  dict(label='Planta',items=[
   I('08-planta-p1-terreo.jpg',('Térreo','sala, cozinha, lavatório, banho e deck'),'Planta humanizada do térreo','half',r='4/5'),
   I('09-planta-p2-loft.jpg',('Loft','sobre a sala'),'Planta humanizada do loft','half',r='4/5')])]),

dict(slug='chale-viver',name='Chalé Viver',cat='chalé',cat_label='chalés',cat_plural='chalés',city='Marília · SP',sub='alvenaria · 88 m²',ref='o Chalé Viver',
 card=dict(src=C+'04-render-fachada-frontal.jpg',focus=(.5,.5),alt='Casa térrea em L com garagem sob pergolado metálico preto'),
 hero=dict(src=C+'01a-frente-garagem-pergolado.jpg',pos='50% 50%',alt='Frente da casa, com a garagem sob pergolado metálico preto'),
 lead='Casa térrea em L no platô do fundo do lote, <b>3 m acima do portão.</b>',
 text=['Uma rampa de concreto sobe até a garagem, coberta por um pergolado metálico preto com acrílico. A casa foi posicionada a 1,20 m da mureta que protege a mangueira existente.',
       'Estar, jantar e cozinha em 43,66 m², suíte com closet e área de serviço. A cobertura é em telha de concreto cinza, em três corpos de duas águas.',
       'Aqui o sistema é o convencional: estacas escavadas, blocos, pilares, vigas e laje treliçada.'],
 ficha=[('Local','Marília · SP'),('Área construída','87,88 m²'),('Projeção','10,25 × 15,45 m'),('Sistema','Alvenaria com estrutura de concreto armado'),('Fundação','Estacas escavadas de 32 cm e blocos'),
        ('Laje','Treliçada, h = 16 cm, concreto C25'),('Cobertura','Telha de concreto, inclinação de 35%'),('Escopo','Arquitetura, estrutural, complementares e projeto legal'),('Etapa','Projeto · 2026')],
 sections=[
  dict(label='Fachadas',items=[
   I('01b-fundos-deck-ombrelone.jpg',('Fundos','deck sob pergolado e a mangueira no alto do talude'),'Fundos da casa, com o deck e a mangueira existente','full'),
   I('02-vista-aerea.jpg',('Vista aérea','casa em L de 10,25 × 15,45 m'),'Vista aérea da casa em L com cobertura de telha de concreto'),
   I('06-render-fundos.jpg',('Deck','porta de correr da sala aberta para o pergolado'),'Fundos com a porta de correr aberta para o deck',pos='55% 50%')]),
  dict(label='Interiores',items=[
   I('07-render-estar-jantar.jpg',('Estar e jantar','43,66 m² integrados à cozinha'),'Estar e jantar com a cozinha ao fundo','full'),
   I('09-render-suite.jpg',('Suíte','18,52 m² com closet'),'Suíte com cama de casal e porta de correr'),
   I('08-render-area-servico.jpg',('Área de serviço','5,73 m²'),'Área de serviço com tanque duplo e armários brancos')]),
  dict(label='Planta e corte',items=[
   I('10-planta-humanizada.jpg',('Planta','casa em L, com a garagem no encontro das alas'),'Planta humanizada da casa em L','plan'),
   I('12a-corte-aa.jpg',('Corte AA','pela suíte e pela sala'),'Corte AA com níveis do piso, da laje e da cumeeira','plan')])]),

dict(slug='chale-analandia',name='Chalé Analândia',cat='chalé',cat_label='chalés',cat_plural='chalés',city='Analândia · SP',sub='steel framing · 132 m²',ref='o Chalé Analândia',
 card=dict(src=C+'03-fachada-norte.jpg',draw='panel',fam='b',alt='Desenho da fachada norte da cabana A-frame'),
 hero=dict(src=C+'03-fachada-norte.jpg',draw='panel',fam='b',alt='Fachada norte: o triângulo do A-frame com o pano de vidro e o volume anexo'),
 lead='Cabana A-frame de dois pavimentos em steel framing, <b>com piscina e churrasqueira.</b>',
 text=['O triângulo tem 7,00 m de base por 7,00 m de altura. No térreo ficam sala, cozinha, lavanderia e banheiro. No pavimento superior, a +2,75 m, a suíte.',
       'Paredes e laje são em light steel frame. A piscina e o telheiro da churrasqueira seguem em concreto armado, com cobertura de madeira no telheiro.'],
 ficha=[('Local','Analândia · SP'),('Área total','132,03 m²'),('Casa','90,39 m² em dois pavimentos'),('Telheiros e piscina','23,64 m² + 18,00 m²'),('Terreno','630 m²'),
        ('Sistema','Steel framing, paredes e laje em LSF'),('Cobertura','Metálica, 91,69 m²'),('Escopo','Projeto executivo e projeto legal'),('Etapa','Projeto · 2025')],
 sections=[
  dict(label='Plantas',items=[
   I('01-planta-layout-terreo.jpg',('Térreo','sala, cozinha, lavanderia e banheiro'),'Planta de layout do térreo','plan half'),
   I('02-planta-layout-superior.jpg',('Pavimento superior','suíte e banheiro'),'Planta de layout do pavimento superior','plan half')]),
  dict(label='Fachadas',items=[
   I('04-fachada-sul.jpg',('Fachada sul','A-frame e volume de dois pavimentos'),'Desenho da fachada sul','plan half'),
   I('05-fachada-oeste.jpg',('Fachada oeste','9,35 m de comprimento'),'Desenho da fachada oeste','plan half')]),
  dict(label='Cortes',items=[
   I('07-corte-aa.jpg',('Corte A-A','transversal, pelo A-frame'),'Corte transversal pelo A-frame','plan half'),
   I('08-corte-bb.jpg',('Corte B-B','longitudinal, pela escada'),'Corte longitudinal, com escada e níveis','plan half')])]),

dict(slug='patio-escolar',assets='escolas',name='Cobertura de pátio escolar',cat='estrutura',cat_label='estruturas',cat_plural='estruturas',city='Papanduva · SC',sub='estrutura metálica · 784 m²',ref='a cobertura de pátio escolar',
 card=dict(src=C+'01-capa.jpg',focus=(.5,.4),alt='Vista sob a cobertura metálica do pátio, com tesouras treliçadas'),
 hero=dict(src=C+'01-capa.jpg',pos='50% 40%',alt='Vista sob a cobertura metálica do pátio, com tesouras treliçadas, terças e pilares'),
 lead='Cobertura metálica para o pátio de duas escolas: <b>784 m² cobertos com 20,2 t de aço.</b>',
 text=['Coberturas de duas águas com faixas de telha translúcida, apoiadas em tesouras treliçadas e pilares metálicos entre os blocos existentes.',
       'A estrutura foi calculada em modelo 3D com 1.175 barras e detalhada em 33 pranchas, das fundações às ligações.'],
 ficha=[('Local','Papanduva · SC'),('Área coberta','784 m²'),('Sistema','Estrutura metálica'),('Aço','20,2 t'),('Tesouras','13'),('Modelo de cálculo','1.175 barras'),
        ('Projeto executivo','33 pranchas'),('Escopo','Estrutura metálica e fundações'),('Etapa','Projeto · 2026')],
 sections=[
  dict(label='Coberturas',items=[
   I('02-aerea.jpg',('Primeira escola','duas águas com faixas translúcidas'),'Vista aérea da cobertura entre os blocos da escola'),
   I('08-segunda-escola.jpg',('Segunda escola','a cobertura mais longa'),'Vista aérea da cobertura da segunda escola')]),
  dict(label='Estrutura',items=[
   I('04-estrutura.jpg',('Sem as telhas','tesouras, terças e contraventamentos'),'Estrutura metálica vista de cima, sem as telhas'),
   I('03-tesouras.jpg',('Tesouras','treliçadas, em sequência'),'Tesouras treliçadas vistas de frente sob a cobertura'),
   I('09-diagonal.jpg',('Pilares','fileira com placas de base'),'Vista em diagonal sob a cobertura, com a fileira de pilares'),
   I('07-corte.jpg',('Borda em corte','telha, perfil de borda e terças'),'Corte da borda da cobertura com as faces cortadas em laranja')]),
  dict(label='Ligações',items=[
   I('05-apoio-zoom.jpg',('Apoio','ligação parafusada no topo do pilar'),'Ligação parafusada entre pilar, tesoura e vigas'),
   I('06-base-zoom.jpg',('Base','placa de base e chumbadores'),'Placa de base do pilar com chumbadores')])]),

dict(slug='cobertura-recife',assets='bcb-recife',name='Cobertura de estacionamento',cat='estrutura',cat_label='estruturas',cat_plural='estruturas',city='Recife · PE',sub='estrutura metálica · 1.437 m²',ref='a cobertura de estacionamento',
 card=dict(src=C+'06-descida.jpg',focus=(.5,.45),alt='Vista por baixo da cobertura metálica, com pilar e mãos-francesas'),
 hero=dict(src=C+'06-descida.jpg',pos='50% 42%',alt='Vista por baixo da cobertura, com pilar, mãos-francesas e a descida pluvial'),
 lead='Nove coberturas metálicas de estacionamento: <b>1.437 m² cobertos com 34 t de aço.</b>',
 text=['As coberturas contornam um edifício existente. A estrutura foi calculada em um modelo global com 1.330 barras.',
       'A drenagem pluvial entrou no mesmo projeto: calhas de PVC entre os perfis da estrutura e descidas presas aos pilares.'],
 ficha=[('Local','Recife · PE'),('Área coberta','1.437 m²'),('Sistema','Estrutura metálica'),('Aço','34 t'),('Coberturas','9'),('Modelo de cálculo','1.330 barras'),
        ('Projeto executivo','32 pranchas'),('Escopo','Estrutura metálica e drenagem pluvial'),('Etapa','Projeto · 2026')],
 sections=[
  dict(label='Coberturas',items=[
   I('03-corredor.jpg',('Corredor','circulação entre duas coberturas'),'Corredor de circulação entre duas coberturas',pos='50% 70%'),
   I('05-agua-furtada.jpg',('Água furtada','encontro de duas águas'),'Telha metálica no encontro de duas águas'),
   I('02-planta-estrutura.jpg',('Planta de cobertura','a malha da estrutura sobre as nove coberturas'),'Planta de cobertura com a malha da estrutura metálica','plan')]),
  dict(label='Drenagem',items=[
   I('04-corte-calha.jpg',('Calha em corte','PVC entre os perfis da estrutura'),'Corte do beiral mostrando a calha de PVC'),
   I('07-descida-abracadeira.jpg',('Descida','tubo preso ao pilar por abraçadeira'),'Abraçadeira que prende o tubo de descida ao pilar')]),
  dict(label='Fixação',items=[
   I('08-lado-alto.jpg',('Lado alto','telha trapezoidal'),'Lado alto da cobertura com a telha trapezoidal'),
   I('09-lado-alto-parafuso.jpg',('Parafuso','fixação da telha'),'Parafuso de fixação da telha')])]),

dict(slug='le-blanc-lofts',name='Le Blanc Lofts',cat='estrutura',cat_label='estruturas',cat_plural='estruturas',city='Angra dos Reis · RJ',sub='light steel frame · off-site',ref='o projeto dos lofts',
 card=dict(src=C+'06-vista-3d-lsf.jpg',draw='panel',fam='b',alt='Vista 3D da estrutura do loft em light steel frame'),
 hero=dict(src=C+'06-vista-3d-lsf.jpg',draw='panel',fam='b',alt='Vista 3D da estrutura completa em light steel frame, com tesouras, laje do mezanino e escada'),
 lead='Loft com mezanino em light steel frame, <b>detalhado para fabricação fora do canteiro.</b>',
 text=['Cada painel tem a sua folha, com lista de corte: 25 painéis de parede, treliças e lajes. A escada interna também é em steel frame.',
       'São 1.393,54 kg de aço em 37 folhas. Os painéis são ancorados ao radier por chumbadores a cada 800 mm, no eixo dos montantes.'],
 ficha=[('Local','Angra dos Reis · RJ'),('Sistema','Light steel frame, fabricação off-site'),('Níveis','Térreo, mezanino e cobertura'),('Altura','6,00 m'),('Aço','1.393,54 kg'),
        ('Conjuntos','Painéis P1 a P25, treliças T1 a T3 e lajes L1 a L6'),('Ancoragem','Chumbador 10 × 75 mm a cada 800 mm'),('Projeto','37 folhas'),('Escopo','Projeto estrutural em steel frame'),('Etapa','Projeto · 2026')],
 sections=[
  dict(label='Plantas',items=[
   I('01-planta-terreo-lsf.jpg',('Térreo','painéis identificados por código'),'Planta do térreo com os painéis em LSF identificados','plan half'),
   I('02-planta-mezanino-lsf.jpg',('Mezanino','lajes, treliças e degraus da escada'),'Planta do mezanino com lajes e treliças em cores','plan half')]),
  dict(label='Cortes',items=[
   I('04-corte-transversal-lsf.jpg',('Corte transversal','tesoura, mezanino e escada'),'Corte da estrutura com tesoura, laje do mezanino e escada','plan half'),
   I('05-corte-longitudinal-lsf.jpg',('Corte longitudinal','ao longo da escada'),'Corte da estrutura ao longo da escada','plan half')]),
  dict(label='Detalhe',items=[
   I('07-detalhe-longarinas-escada.jpg',('Longarinas da escada','duplo box 200 #0,95'),'Detalhe da fixação das longarinas da escada nos painéis e no radier','plan')])]),

dict(slug='do-aco-a-estrutura',assets='estrutura-bh',name='Do aço à estrutura',cat='estrutura',cat_label='estruturas',cat_plural='estruturas',city='Belo Horizonte · MG',sub='light steel frame · 600 kg',ref='o projeto de Belo Horizonte',
 card=dict(src=C+'01-estrutura-completa.jpg',focus=(.5,.5),fam='c',alt='Modelo 3D de uma estrutura em steel frame'),
 hero=dict(src=C+'01-estrutura-completa.jpg',pos='50% 45%',fam='c',alt='Modelo 3D da estrutura completa em steel frame, com painéis de parede, treliças e cobertura'),
 lead='430 peças. <b>Nenhuma medida decidida na obra.</b>',
 text=['Num steel frame, o aço é comprado e cortado pelo projeto. O plano de corte escolheu, barra a barra, entre a de 3 m e a de 6 m, contando 3 mm de serra por peça e 10 mm de ponta por barra.',
       'Das 77 barras, 32 saíram sem sobra nenhuma. A perda foi de 9,5 kg em 651,3 kg comprados.',
       'Na obra, cada painel tem a sua folha: 22 folhas no caderno de montagem. O nome no painel é o nome da folha.'],
 ficha=[('Local','Belo Horizonte · MG'),('Sistema','Light steel frame'),('Peças','430'),('Aço na estrutura','600 kg'),('Barras de corte','77, sendo 32 sem sobra'),('Perda no corte','1,5%'),
        ('Caderno de montagem','22 folhas para 15 painéis e tesouras'),('Escopo','Projeto estrutural, plano de corte e caderno de montagem'),('Etapa','Projeto · 2026')],
 sections=[
  dict(label='Plano de corte',items=[I('02-plano-de-corte-77-barras.jpg',('77 barras','uma barra por linha, cada cor uma peça'),'Gráfico do plano de corte com as 77 barras divididas em peças','full')]),
  dict(label='Montagem',items=[
   I('03-montagem-etapa-1.jpg',('Primeiros painéis','paredes'),'Primeiros painéis de parede no lugar'),
   I('04-montagem-etapa-2.jpg',('Paredes','painel a painel'),'Mais painéis de parede posicionados'),
   I('05-montagem-etapa-3.jpg',('Painel superior','descendo sobre as paredes'),'Painel superior descendo sobre as paredes'),
   I('06-montagem-cobertura.jpg',('Cobertura','o último painel'),'Último painel de cobertura descendo sobre a estrutura')])]),
]

# família de cada imagem (padrão: 'a' = render em cor graduada; 'b' = desenho em tinta; 'c' = modelo de estrutura em fundo escuro)
FAM={
 'taquaracu':{'07-planta-baixa.jpg':'b','08-fundacao-e-estrutura.jpg':'c','12-telha-sanduiche.jpg':'c'},
 'chale-acolher':{'04-render-lateral-direita-lavanderia.jpg':'c','05-render-interior-corte-layout.jpg':'c','06-render-estrutura-lsf.jpg':'c','08-lsf-3d-frente.jpg':'b','10-lsf-3d-sem-cobertura.jpg':'b'},
 'chale-viver':{'12a-corte-aa.jpg':'b'},
 'chale-analandia':{k:'b' for k in ('01-planta-layout-terreo.jpg','02-planta-layout-superior.jpg','04-fachada-sul.jpg','05-fachada-oeste.jpg','07-corte-aa.jpg','08-corte-bb.jpg')},
 'le-blanc-lofts':{k:'b' for k in ('01-planta-terreo-lsf.jpg','02-planta-mezanino-lsf.jpg','04-corte-transversal-lsf.jpg','05-corte-longitudinal-lsf.jpg','07-detalhe-longarinas-escada.jpg')},
 'estrutura-bh':{k:'c' for k in ('03-montagem-etapa-1.jpg','04-montagem-etapa-2.jpg','05-montagem-etapa-3.jpg','06-montagem-cobertura.jpg')},
}
