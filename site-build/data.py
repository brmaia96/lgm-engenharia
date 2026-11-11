import importlib.util,os
_s=importlib.util.spec_from_file_location('sp',os.path.dirname(__file__)+'/static_pages.py'); _m=importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
SOBRE_BODY=_m.SOBRE_BODY; AGENDA_BODY=_m.agenda_body()
_si=importlib.util.spec_from_file_location('inss_page',os.path.dirname(__file__)+'/inss_page.py'); INSS=importlib.util.module_from_spec(_si); _si.loader.exec_module(INSS)
OBRAS_META='casas, chalés, salas comerciais e estruturas em aço'
HOME_SELECT=['casa-taquaracu','salas-comerciais','casa-do-bosque']
CMP_CAPTION='<b><a href="o-casa-taquaracu.html">Casa Taquaraçu</a></b><span>arraste para ver a estrutura</span>'
C='clean/'
def I(src,cap,alt,lay='half',**k): d=dict(src=C+src,cap=cap,alt=alt,lay=lay); d.update(k); return d

PROJECTS=[
dict(slug='casa-taquaracu',assets='taquaracu',ref='a Casa Taquaraçu',name='Casa Taquaraçu',cat='casa',cat_label='casas',cat_plural='casas',city='Taquaraçu de Minas, MG',sub='steel frame · 296 m²',
 card=dict(src=C+'01-capa-aerea.jpg',focus=(.45,.6),alt='Vista aérea da Casa Taquaraçu, com piscina entre a casa e a edícula'),
 hero=dict(src=C+'01-capa-aerea.jpg',pos='50% 62%',alt='Vista aérea da casa e da edícula, com a piscina entre os dois blocos e a serra ao fundo'),
 lead='Casa e edícula em steel frame <b>numa encosta da serra mineira.</b>',
 text=['A edícula fica 1,35 m abaixo da casa. A varanda avança sobre o desnível e, entre os dois blocos, uma piscina de 27 m² ocupa o terraço.',
       'Por dentro, estar, jantar e cozinha formam um só ambiente de 86,90 m² sob a inclinação do telhado, coberto com telha sanduíche.',
       'O trabalho foi o projeto executivo, os complementares e a compatibilização de tudo com a estrutura: <b>11 modelos conversando entre si antes de a obra começar.</b>'],
 ficha=[('Local','Taquaraçu de Minas, MG'),('Área construída','296,35 m²'),('Casa e edícula','198,72 m² + 97,63 m²'),('Terreno','1.463 m²'),('Sistema','Light steel frame'),
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
  dict(label='Estrutura',items=[
   I('08-fundacao-e-estrutura.jpg',('Estrutura em steel frame','radier sobre pilares · modelo 3D completo'),'Modelo 3D da estrutura em steel frame sobre laje apoiada em pilares','full',pos='50% 52%'),
   I('10-steel-frame-por-dentro.jpg',('Steel frame por dentro','montantes, painéis e treliças de cobertura'),'Vista interna do modelo da estrutura em steel frame'),
   I('11-estrutura-e-instalacoes.jpg',('Estrutura e instalações','11 modelos compatibilizados'),'Painéis de steel frame com as instalações sobrepostas em cores')])]),

dict(slug='chale-acolher',name='Chalé Acolher',cat='chalé',cat_label='chalés',cat_plural='chalés',city='Marília, SP',sub='steel frame · 81 m²',ref='o Chalé Acolher',
 card=dict(src=C+'00-fachada-frontal-pergolado.jpg',focus=(.5,.55),alt='Fachada do Chalé Acolher, em telha metálica creme, com garagem sob pergolado'),
 hero=dict(src=C+'00-fachada-frontal-pergolado.jpg',pos='50% 58%',alt='Fachada frontal do chalé, com paredes e cobertura em telha metálica creme'),
 lead='Chalé térreo com <b>a mesma telha metálica creme nas paredes e no telhado.</b>',
 text=['A sala junta estar, jantar e cozinha em 33,54 m² e abre para os fundos por uma porta de correr de 3,00 m. Suíte com closet, um dormitório que também é escritório e lavanderia externa junto à divisa.',
       'A estrutura é em light steel frame painelizado, com <b>um só perfil em toda a obra:</b> paredes em módulo de 0,40 m, tesouras alinhadas aos montantes e laje técnica em vigas treliçadas.'],
 ficha=[('Local','Marília, SP'),('Área construída','80,57 m²'),('Projeção','7,10 × 10,65 m'),('Sistema','Light steel frame painelizado'),('Perfil','ME 90 #0,95, único em toda a estrutura'),
        ('Módulo','Montantes a cada 0,40 m'),('Fechamento','Telha metálica trapezoidal RT 45 em parede e cobertura'),('Vento de projeto','V0 = 40 m/s, categoria III'),
        ('Escopo','Arquitetura, estrutural em steel frame, complementares e caderno de montagem'),('Etapa','Projeto · 2026')],
 sections=[
  dict(label='Fachadas',items=[
   I('01-fundos-porta-de-correr.jpg',('Fundos','porta de correr de 3,00 m'),'Fundos do chalé, com a porta de correr da sala','full',pos='50% 36%'),
   I('03-render-fachada-frontal-lateral.jpg',('Fundos e lateral','porta de entrada e porta de correr da sala'),'Maquete do chalé: a lateral com a porta de entrada e a empena dos fundos com a porta de correr',r='16/9'),
   I('04-render-lateral-direita-lavanderia.jpg',('Lateral direita','janela em fita e lavanderia externa'),'Maquete do chalé pela lateral direita, com a janela em fita e o volume da lavanderia',r='16/9')]),
  dict(label='Interiores',items=[
   I('14-a3-interna-estar.jpg',('Estar','sala integrada de 33,54 m²'),'Estar visto da cozinha, com a ilha em primeiro plano','full'),
   I('15-a3-interna-cozinha-jantar.jpg',('Cozinha e jantar','ilha com cooktop'),'Cozinha e jantar com mesa de madeira para seis lugares'),
   I('16-a3-interna-suite.jpg',('Suíte','9,15 m² · porta de correr para o gramado'),'Suíte com cama de casal e porta de correr de vidro'),
   I('18-a3-interna-dormitorio-escritorio.jpg',('Dormitório e escritório','7,80 m²'),'Dormitório com bancada de parede a parede'),
   I('24-a3-interna-banho-social.jpg',('Banho social','3,12 m²'),'Banho social com bancada escura e cuba embutida')]),
  dict(label='Estrutura',items=[
   I('06-render-estrutura-lsf.jpg',('Estrutura em steel frame','painéis de parede, tesouras e cobertura · um só perfil'),'Estrutura completa em steel frame, com painéis de parede e tesouras','full')])]),

dict(slug='chale-piedade',name='Chalé Piedade',cat='chalé',cat_label='chalés',cat_plural='chalés',city='Piedade, SP',sub='A-frame · 70 m²',ref='o Chalé Piedade',
 card=dict(src=C+'02-fachada-nordeste-hall.jpg',focus=(.5,.5),alt='Chalé A-frame com cobertura grafite e hall em ripado de madeira'),
 hero=dict(src=C+'02-fachada-nordeste-hall.jpg',pos='50% 55%',alt='Chalé A-frame na golden hour, com cobertura de junta elevada grafite e hall em ripado'),
 lead='Chalé A-frame de serra, <b>com a empena norte inteira em vidro.</b>',
 text=['Um triângulo de 62° sobre embasamento de concreto. A sala tem pé-direito duplo, lareira suspensa e escada caracol até o mezanino, onde fica o quarto.',
       'A cobertura é em telha metálica de junta elevada, com juntas a cada 45 cm. A empena sul e o hall de entrada são em ripado de madeira.'],
 ficha=[('Local','Piedade, SP'),('Área','70,35 m²'),('Projeção','6,40 × 9,05 m'),('Forma','A-frame a 62°'),('Níveis','Térreo e mezanino a +2,65 m'),
        ('Cobertura','Telha metálica de junta elevada'),('Mezanino','Laje em light steel frame'),('Embasamento','Concreto aparente, 1,05 m'),('Escopo','Projeto de arquitetura'),('Etapa','Projeto')],
 sections=[
  dict(label='Fachadas',items=[
   I('01-fachada-norte-hora-azul.jpg',('Empena norte','vidro de ponta a ponta, voltado para o deck'),'Empena de vidro na hora azul, com o interior aceso','full'),
   I('03-aerea.jpg',('Implantação','deck com ofurô'),'Vista aérea do chalé com o deck e o ofurô','full')]),
  dict(label='Interiores',items=[
   I('04-interna-pe-direito-duplo.jpg',('Sala','pé-direito duplo, mezanino e escada caracol'),'Sala com pé-direito duplo e mezanino com guarda-corpo de vidro','full'),
   I('05-interna-cozinha-jantar.jpg',('Cozinha e jantar','11,69 m² sob o mezanino'),'Cozinha e mesa de jantar sob o mezanino'),
   I('06-interna-mezanino-para-vidro.jpg',('Mezanino','quarto de 14,61 m² voltado para o vidro'),'Vista do mezanino para a empena triangular de vidro'),
   I('07-interna-lareira.jpg',('Lareira suspensa','no centro da sala'),'Lareira suspensa preta com fogo aceso'),
   I('08-interna-banheiro.jpg',('Banheiro','3,05 m²'),'Banheiro com paredes em tom cimento e cuba de apoio')])]),

dict(slug='casa-duo',name='Casa Duo',cat='casa',cat_label='casas',cat_plural='casas',city='Marília, SP',sub='casa térrea · 120 m²',ref='a Casa Duo',
 # Conferência (nov/2026): das nove imagens do kit só duas seguem o modelo (quintal e suíte, com recorte). Capa e cobertura são
 # quadros do próprio modelo (1020 px). Fachada, aérea, piscina, cozinha e estar não entram: contradizem o modelo ou mudam entre vistas.
 card=dict(src='proj/modelo-01-volumetria.png',focus=(.5,.5),alt='Maquete do modelo da Casa Duo: casa térrea com platibanda, em dois lotes'),
 hero=dict(src='proj/modelo-01-volumetria.png',pos='50% 50%',alt='Maquete do modelo: casa térrea com platibanda ocupando os dois lotes, vista do canto da frente'),
 lead='Dois lotes unificados <b>viraram uma casa térrea com piscina.</b>',
 text=[],
 ficha=[('Local','Marília, SP'),('Área','119,82 m²'),('Sistema','Alvenaria e concreto armado'),('Escopo','Projeto arquitetônico e processo na prefeitura'),('Etapa','Projeto · 2026')],
 sections=[
  dict(label='Quintal e suíte',items=[
   dict(src='recortes/externa-quintal-ia-recorte-1x1-sem-vizinhos.jpg',cap=('Quintal',''),alt='Quintal: porta de correr da sala, janela da cozinha e canto da piscina',lay='half'),
   dict(src='recortes/interna-suite-ia-recorte-4x3.jpg',cap=('Suíte',''),alt='Suíte com a janela na parede lateral',lay='half')]),
  dict(label='Cobertura',items=[
   dict(src='proj/modelo-04-corte-cobertura.png',cap=('Estrutura da cobertura',''),alt='Modelo cortado na altura da cobertura, com a estrutura metálica do telhado e a caixa-d\'água',lay='plan')])]),

dict(slug='tiny-house',name='Tiny House',cat='chalé',cat_label='chalés',cat_plural='chalés',city='Sorocaba, SP',sub='duas águas · 39 m²',ref='a Tiny House',
 card=dict(src=C+'02-fachada-lateral-monolito.jpg',focus=(.5,.5),alt='Tiny house em telha metálica grafite, com frente de vidro e deck'),
 hero=dict(src=C+'02-fachada-lateral-monolito.jpg',pos='50% 55%',alt='Volume de telha metálica grafite contínua em parede e cobertura, com frente de vidro'),
 lead='39 m² em duas águas, <b>com a telha dobrando da cobertura para a parede.</b>',
 text=['Uma casca de telha metálica de junta elevada, sem beiral, emoldurada por um portal preto. A frente é toda de vidro e abre para o deck.',
       'No térreo ficam sala, cozinha e banho. O loft de dormir fica sobre a cozinha e o banho, com uma claraboia em cima da cama; a sala tem pé-direito duplo e acesso por escada de degraus alternados.'],
 ficha=[('Local','Sorocaba, SP'),('Área','38,57 m²'),('Projeção','4,00 × 7,50 m'),('Forma','Duas águas a 53°'),('Níveis','Térreo e loft a +2,60 m'),
        ('Fechamento','Telha metálica de junta elevada em parede e cobertura'),('Frente','Porta de correr de vidro, 3,70 × 2,40 m'),('Deck','4,00 × 2,00 m'),('Escopo','Projeto de arquitetura'),('Etapa','Projeto')],
 sections=[
  dict(label='Fachadas',items=[
   I('01-fachada-frontal-hora-azul.jpg',('Frente','vidro de ponta a ponta, emoldurado pelo portal'),'Frente de vidro na hora azul, com o interior aceso','full'),
   I('03-aerea.jpg',('Cobertura','claraboia sobre a cama'),'Vista aérea com o deck e a claraboia'),
   I('07-fachada-fundo-ripado-noturna.jpg',('Fundo','oitão em ripado de madeira'),'Oitão posterior em ripado iluminado à noite')]),
  dict(label='Interiores',items=[
   I('04-interna-sala-para-vidro.jpg',('Sala','9,73 m² voltados para o vidro'),'Interior voltado para a frente de vidro','full'),
   I('05-interna-loft.jpg',('Loft','14,65 m² · cama sob a claraboia'),'Loft com a cama sob a claraboia'),
   I('06-interna-cozinha-escada.jpg',('Cozinha e escada','degraus alternados'),'Cozinha em L e escada de degraus alternados')])]),

dict(slug='chale-viver',name='Chalé Viver',cat='chalé',cat_label='chalés',cat_plural='chalés',city='Marília, SP',sub='alvenaria · 88 m²',ref='o Chalé Viver',
 card=dict(src=C+'04-render-fachada-frontal.jpg',focus=(.5,.5),alt='Casa térrea em L com garagem sob pergolado metálico preto'),
 hero=dict(src=C+'04-render-fachada-frontal.jpg',pos='50% 62%',alt='Frente da casa, com a garagem sob pergolado metálico preto'),
 lead='Casa térrea em L no platô do fundo do lote, <b>3 m acima do portão.</b>',
 text=['Uma rampa de concreto sobe até a garagem, coberta por um pergolado metálico preto com acrílico. A casa foi posicionada a 1,20 m da mureta que protege a mangueira existente.',
       'Estar, jantar e cozinha em 43,66 m², suíte com closet e área de serviço. A cobertura é em telha de concreto cinza, em três corpos de duas águas.',
       'Aqui o sistema é o convencional: estacas escavadas, blocos, pilares, vigas e laje treliçada.'],
 ficha=[('Local','Marília, SP'),('Área construída','87,88 m²'),('Projeção','10,25 × 15,45 m'),('Sistema','Alvenaria com estrutura de concreto armado'),('Fundação','Estacas escavadas de 32 cm e blocos'),
        ('Laje','Treliçada, h = 16 cm, concreto C25'),('Cobertura','Telha de concreto, inclinação de 35%'),('Escopo','Arquitetura, estrutural, complementares e projeto legal'),('Etapa','Projeto · 2026')],
 sections=[
  dict(label='Fachadas',items=[
   I('06-render-fundos.jpg',('Fundos','deck sob pergolado e a mangueira no alto do talude'),'Fundos da casa, com o deck sob pergolado e a mangueira existente','full',pos='55% 45%'),
   I('04-render-fachada-frontal.jpg',('Frente','garagem sob pergolado metálico preto'),'Frente da casa, com a garagem sob o pergolado metálico'),
   I('02-vista-aerea.jpg',('Vista aérea','casa em L de 10,25 × 15,45 m'),'Vista aérea da casa em L com cobertura de telha de concreto',pos='50% 45%')]),
  dict(label='Interiores',items=[
   I('07-render-estar-jantar.jpg',('Estar e jantar','43,66 m² integrados à cozinha'),'Estar e jantar com a cozinha ao fundo','full'),
   I('09-render-suite.jpg',('Suíte','18,52 m² com closet'),'Suíte com cama de casal e porta de correr'),
   I('08-render-area-servico.jpg',('Área de serviço','5,73 m²'),'Área de serviço com tanque duplo e armários brancos')])]),

dict(slug='chale-analandia',name='Chalé Analândia',cat='chalé',cat_label='chalés',cat_plural='chalés',city='Analândia, SP',sub='steel frame · 132 m²',ref='o Chalé Analândia',
 card=dict(src=C+'03-fachada-norte.jpg',draw='panel',fam='b',alt='Desenho da fachada norte da cabana A-frame'),
 hero=dict(src=C+'03-fachada-norte.jpg',draw='panel',fam='b',alt='Fachada norte: o triângulo do A-frame com o pano de vidro e o volume anexo'),
 lead='Cabana A-frame de dois pavimentos em steel frame, <b>com piscina e churrasqueira.</b>',
 text=['O triângulo tem 7,00 m de base por 7,00 m de altura. No térreo ficam sala, cozinha, lavanderia e banheiro. No pavimento superior, a +2,75 m, a suíte.',
       'Paredes e laje são em light steel frame. A piscina e o telheiro da churrasqueira seguem em concreto armado, com cobertura de madeira no telheiro.'],
 ficha=[('Local','Analândia, SP'),('Área total','132,03 m²'),('Casa','90,39 m² em dois pavimentos'),('Telheiros e piscina','23,64 m² + 18,00 m²'),('Terreno','630 m²'),
        ('Sistema','Light steel frame, paredes e laje'),('Cobertura','Metálica, 91,69 m²'),('Escopo','Projeto executivo e projeto legal'),('Etapa','Projeto · 2025')],
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

dict(slug='patio-escolar',assets='escolas',name='Cobertura de pátio escolar',cat='estrutura',cat_label='estruturas',cat_plural='estruturas',city='Papanduva, SC',sub='estrutura metálica · 784 m²',ref='a cobertura de pátio escolar',
 card=dict(src=C+'01-capa.jpg',crop=(0,.06,1,.94),focus=(.5,.4),alt='Vista sob a cobertura metálica do pátio, com tesouras treliçadas'),
 hero=dict(src=C+'01-capa.jpg',crop=(0,.06,1,.94),pos='50% 40%',alt='Vista sob a cobertura metálica do pátio, com tesouras treliçadas, terças e pilares'),
 lead='Cobertura metálica para o pátio de duas escolas: <b>784 m² cobertos com 20,2 t de aço.</b>',
 text=['Coberturas de duas águas com faixas de telha translúcida, apoiadas em tesouras treliçadas e pilares metálicos entre os blocos existentes.',
       'A estrutura foi calculada em modelo 3D com 1.175 barras e detalhada em 33 pranchas, das fundações às ligações.'],
 ficha=[('Local','Papanduva, SC'),('Área coberta','784 m²'),('Sistema','Estrutura metálica'),('Aço','20,2 t'),('Tesouras','13'),('Modelo de cálculo','1.175 barras'),
        ('Projeto executivo','33 pranchas'),('Escopo','Estrutura metálica e fundações'),('Etapa','Projeto · 2026')],
 sections=[
  dict(label='Coberturas',items=[
   I('02-aerea.jpg',('Primeira escola','duas águas com faixas translúcidas'),'Vista aérea da cobertura entre os blocos da escola'),
   I('08-segunda-escola.jpg',('Segunda escola','a cobertura mais longa'),'Vista aérea da cobertura da segunda escola')]),
  dict(label='Estrutura',items=[
   I('04-estrutura.jpg',('Sem as telhas','tesouras, terças e contraventamentos'),'Estrutura metálica vista de cima, sem as telhas','third'),
   I('03-tesouras.jpg',('Tesouras','treliçadas, em sequência'),'Tesouras treliçadas vistas de frente sob a cobertura','third'),
   I('09-diagonal.jpg',('Pilares','fileira entre os blocos'),'Vista em diagonal sob a cobertura, com a fileira de pilares','third')])]),

dict(slug='le-blanc-lofts',name='Le Blanc Lofts',cat='estrutura',cat_label='estruturas',cat_plural='estruturas',city='Angra dos Reis, RJ',sub='steel frame · fabricação fora do canteiro',ref='o projeto dos lofts',
 card=dict(src=C+'06-vista-3d-lsf.jpg',draw='panel',fam='b',alt='Vista 3D da estrutura do loft em light steel frame'),
 hero=dict(src=C+'06-vista-3d-lsf.jpg',draw='panel',fam='b',alt='Vista 3D da estrutura completa em light steel frame, com tesouras, laje do mezanino e escada'),
 lead='Loft com mezanino em light steel frame, <b>detalhado para fabricação fora do canteiro.</b>',
 text=['Cada painel tem a sua folha, com lista de corte: 25 painéis de parede, treliças e lajes. A escada interna também é em steel frame.',
       'São 1.393,54 kg de aço em 37 folhas. Os painéis são ancorados ao radier por chumbadores a cada 800 mm, no eixo dos montantes.'],
 ficha=[('Local','Angra dos Reis, RJ'),('Sistema','Light steel frame, fabricado fora do canteiro'),('Níveis','Térreo, mezanino e cobertura'),('Altura','6,00 m'),('Aço','1.393,54 kg'),
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

dict(slug='ampliacao-steel-frame',name='Ampliação em steel frame',cat='estrutura',cat_label='estruturas',cat_plural='estruturas',city='Belo Horizonte, MG',sub='steel frame · 600 kg de aço',ref='a ampliação em steel frame',
 # Conferência (nov/2026): a elevação confere com o modelo com erro de até 5 mm. Saem a explodida (objetos soltos, e é diagrama
 # de montagem), o detalhe estourado e a isométrica repetida. A arquitetura é de terceiros: o escopo diz só o que é do escritório.
 card=dict(src=C+'02-estrutura-frente.jpg',focus=(.5,.5),fam='c',alt='Estrutura de uma ampliação em steel frame vista de frente'),
 hero=dict(src=C+'02-estrutura-frente.jpg',draw='night',fam='c',alt='Elevação da estrutura em steel frame: painéis com contraventamento, vão com painel elevado e porta'),
 lead='430 peças. <b>Nenhuma medida decidida na obra.</b>',
 text=[],
 ficha=[('Local','Belo Horizonte, MG'),('Área','11 m² de projeção'),('Sistema','Light steel frame'),('Escopo','Projeto estrutural e caderno de montagem'),('Etapa','Projeto · 2026')],
 sections=[
  dict(label='Estrutura',items=[
   I('03-estrutura-vista-alta.jpg',('Vista alta',''),'Vista alta da estrutura: parede longa, paredes transversais, tesouras e painéis de cobertura','half nat'),
   I('07-modelo-perspectiva-frente.jpg',('Modelo',''),'Perspectiva do modelo de fabricação da estrutura inteira','half nat'),
   I('06-estrutura-interior-laje.jpg',('Por dentro',''),'Vista interna da estrutura, com o painel de piso e a tesoura da cobertura','full',crop=(0,.2,1,.8))])]),
]

# família de cada imagem (padrão: 'a' = render em cor graduada; 'b' = desenho em tinta; 'c' = modelo de estrutura em fundo escuro;
# 'd' = render em cor sobre fundo de estúdio escuro)
FAM={
 'taquaracu':{'07-planta-baixa.jpg':'b','08-fundacao-e-estrutura.jpg':'c','12-telha-sanduiche.jpg':'c'},
 'chale-acolher':{'03-render-fachada-frontal-lateral.jpg':'d','04-render-lateral-direita-lavanderia.jpg':'d','06-render-estrutura-lsf.jpg':'c'},
 'chale-viver':{'12a-corte-aa.jpg':'b'},
 'le-blanc-lofts':{k:'b' for k in ('42-perspectiva-modelo-frente.jpg','43-perspectiva-modelo-fundos.jpg','44-elevacao-modelo-tres-lofts-acesso.jpg','46-elevacao-modelo-loft-frontal.jpg','25-vista-3d-lsf.jpg')},
 'ampliacao-steel-frame':{k:'c' for k in ('03-estrutura-vista-alta.jpg','07-modelo-perspectiva-frente.jpg','06-estrutura-interior-laje.jpg')},
 'casa-duo':{'modelo-04-corte-cobertura.png':'b'},
 'residencia-ym':{k:'b' for k in ('02-perspectiva-fachada-frontal.jpg','06-vista-aerea-nordeste.jpg','10-interior-cozinha.jpg','09-estrutura-trelicas-cobertura.jpg')},
}


# ---------------------------------------------------------------------------------------------------------
# SELEÇÃO ENXUTA (pedido do cliente): o portfólio só mostra que há know-how. Poucas imagens por projeto,
# só fachada, externa, interna e o 3D da estrutura; ficha curta; no máximo dois parágrafos.
# Os dados completos ficam acima; esta camada escolhe o que vai ao ar.
# Regra do cliente (nov/2026): toda obra abre com fachada RENDERIZADA, em alta, nada de isométrico.
# Casa Duo e Casa da Raia não têm render de fachada fiel ao projeto atual (só vistas isométricas do modelo e imagens de IA
# que mudam o projeto): ficam fora do ar até o cliente mandar renders do modelo atual. Dados prontos abaixo.
HELD=[]   # Casa Duo voltou na v37 com as imagens renderizadas da própria prancha do projeto
# MÍNIMO (instrução do cliente, nov/2026): "fotos obras, só o mínimo e informações básicas, não precisa de tanto detalhe".
# Capa + no máximo quatro imagens por projeto; ficha de cinco linhas; só a frase de abertura, sem parágrafos; legenda só com o nome.
LEAN={
 # Conferência independente (nov/2026): cada imagem no ar foi comparada com planta, cortes e fachadas do projeto.
 # Só entram as aprovadas; o que a IA redesenhou (edícula da Taquaraçu, externas do Acolher) saiu ou foi recortado.
 'casa-taquaracu':[('Interiores',[('04-','half'),('05-','half')]),('Estrutura',[('10-','full')])],
 'chale-acolher':[('Fachada',[('04-','full')]),('Interiores',[('15-','full')]),('Estrutura',[('06-','full')])],
 'chale-piedade':[('Interiores',[('04-','half'),('06-','half')])],
 'tiny-house':[('Interiores',[('05-','half'),('04-','half')])],
 'chale-viver':[('Fachada',[('06-','full')]),('Interiores',[('07-','half'),('09-','half')])],
 'chale-analandia':[('Fachada',[('20-','full')]),('Interiores',[('24-','full')])],
 'salas-comerciais':[('Externas',[('03-','half'),('04-','half')])],
 'patio-escolar':[('Coberturas',[('02-','half'),('08-','half')]),('Estrutura',[('04-','full')])],
}
FICHA_KEEP={
 'casa-taquaracu':['Local','Área construída','Sistema','Escopo','Etapa'],
 'chale-acolher':['Local','Área construída','Sistema','Escopo','Etapa'],
 'chale-piedade':['Local','Área','Cobertura','Escopo','Etapa'],
 'tiny-house':['Local','Área','Fechamento','Escopo','Etapa'],
 'chale-viver':['Local','Área construída','Sistema','Escopo','Etapa'],
 'chale-analandia':['Local','Área total','Sistema','Escopo','Etapa'],
 'salas-comerciais':['Local','Área construída','Sistema','Escopo','Etapa'],
 'patio-escolar':['Local','Área coberta','Sistema','Escopo','Etapa'],
 'le-blanc-lofts':['Local','Unidades','Sistema','Escopo','Etapa'],
}
TEXT_KEEP={}   # nenhum parágrafo além da frase de abertura
def _lean(P):
    out=[]
    for p in P:
        if p['slug'] in HELD: continue
        if p['slug'] in LEAN:
            pool={it['src'].split('/')[-1]:it for sec in p['sections'] for it in sec['items']}
            secs=[]
            for label,items in LEAN[p['slug']]:
                sel=[]
                for pre,lay in items:
                    k=[n for n in pool if n.startswith(pre)]; assert len(k)==1,(p['slug'],pre,k)
                    it=dict(pool[k[0]]); it['lay']=lay
                    if lay!='half' or not it.get('r'): pass
                    sel.append(it)
                secs.append(dict(label=label,items=sel))
            p=dict(p); p['sections']=secs
        if p['slug'] in FICHA_KEEP:
            keep=FICHA_KEEP[p['slug']]; p=dict(p); p['ficha']=[kv for kv in p['ficha'] if kv[0] in keep]
        p=dict(p); p['text']=[p['text'][i] for i in TEXT_KEEP.get(p['slug'],[])]
        p['ficha']=[('Área' if k.startswith('Área') else k,v) for k,v in p['ficha']]
        p['sections']=[dict(sec,items=[dict(it,cap=(it['cap'][0],'')) for it in sec['items']]) for sec in p['sections']]
        out.append(p)
    return out
# Le Blanc Lofts: só o que é do projeto. Vistas do modelo de arquitetura (prancha 02) e o 3D da estrutura (projeto de LSF).
# As imagens 30 a 41 e a 08 da pasta eram geradas por IA e mudavam o projeto (janela na fachada que não existe,
# layout interno diferente a cada vista). Reclamação direta do cliente: "tem que seguir o projeto, tem que ser real". Não usar.
for _p in PROJECTS:
    if _p['slug']=='le-blanc-lofts':
        # v30: capa = render no Cycles (render/lofts_blender.py) montado com as medidas da implantação, da elevação de acesso e da
        # elevação frontal do modelo Revit e com as cotas do projeto em LSF; conferido em vista ortogonal contra a elevação de acesso.
        # Palmeiras e agaves do paisagismo ficaram fora (não modeladas). Dentro da página, só o 3D da estrutura.
        _p.update(card=dict(src='render/02-fachada-render.png',focus=(.45,.6),alt='Lofts em Angra dos Reis: volume branco com marquise, porta pivotante de madeira e palmeira-imperial no jardim de acesso'),
          hero=dict(src='render/02-fachada-render.png',pos='50% 58%',alt='Acesso dos lofts: volumes brancos de 6 m com platibanda, marquise na largura da fachada, parede de ala, porta pivotante, palmeiras e agaves'),
          lead='Três lofts com mezanino em light steel frame, <b>projetados para fabricação fora do canteiro.</b>',
          text=[],
          sections=[
           dict(label='Estrutura',items=[
            I('25-vista-3d-lsf.jpg',('Estrutura em light steel frame',''),'Vista 3D da estrutura completa do loft em light steel frame','plan')])])
        _p['ficha']=[kv for kv in _p['ficha'] if kv[0]!='Níveis']; _p['ficha'].insert(1,('Unidades','3 lofts de 28,90 m², com térreo e mezanino'))
PROJECTS.insert(next(i for i,_p in enumerate(PROJECTS) if _p['slug']=='patio-escolar'),
 dict(slug='salas-comerciais',assets='comercial-marilia',name='Salas comerciais',cat='comercial',cat_label='comerciais',cat_plural='comerciais',city='Marília, SP',sub='reforma e regularização · 169 m²',ref='o projeto das salas comerciais',
  card=dict(src=C+'02-patio-frontal-cobogo.jpg',focus=(.5,.5),alt='Pátio de entrada das salas comerciais, com muro de cobogó e fachada verde'),
  hero=dict(src=C+'02-patio-frontal-cobogo.jpg',pos='50% 55%',alt='Pátio de entrada com piso amadeirado, muro de cobogó branco e fachada verde'),
  lead='Uma casa virou salas comerciais, <b>com projeto, regularização e habite-se.</b>',
  text=['Residência térrea convertida em seis salas para locação, com recepção, sala de espera, quatro sanitários, um deles acessível, e estacionamento para seis carros.',
        'O trabalho foi a regularização com reforma, ampliação e mudança de uso: projeto legal, prevenção a incêndio, as built e laudo para o habite-se.'],
  ficha=[('Local','Marília, SP'),('Área construída','169,14 m²'),('Terreno','484 m²'),('Sistema','Alvenaria de blocos de concreto'),
         ('Escopo','Projeto legal, prevenção a incêndio, as built e laudo de habite-se'),('Etapa','Obra concluída · 2026')],
  sections=[
   dict(label='Fachada',items=[I('01-fachada-rua.jpg',('Fachada','muro com cobogó e portão branco'),'Fachada das salas comerciais vista da rua, com muro verde e painéis de cobogó','full',pos='50% 92%')]),
   dict(label='Externas e circulação',items=[
    I('03-patio-frontal-platibanda.jpg',('Pátio frontal','platibanda e moldura da janela'),'Pátio frontal com piso amadeirado e fachada verde','third'),
    I('04-fundos-estacionamento.jpg',('Estacionamento','seis vagas nos fundos'),'Fundos do imóvel com o estacionamento em piso intertravado','third'),
    I('06-circulacao-coberta.jpg',('Circulação coberta','cobertura de vidro e cobogó'),'Circulação lateral com cobertura de vidro e parede de cobogó','third')])]))
# chale-analandia: renders do projeto encontrados no Drive (frente, três quartos com piscina, fundos e dois interiores); sem pranchas.
for _p in PROJECTS:
    if _p['slug']=='chale-analandia':
        _p.update(card=dict(src=C+'21-render.jpg',crop=(0,0,.9,1),focus=(.35,.5),alt='Cabana A-frame com frente de vidro, piscina e área de churrasqueira'),
          hero=dict(src=C+'21-render.jpg',crop=(0,0,.9,1),pos='50% 55%',alt='Cabana A-frame com a frente de vidro voltada para a piscina e a área de churrasqueira ao lado'),
          lead='Cabana A-frame de dois pavimentos em steel frame, <b>com piscina e churrasqueira.</b>',
          text=['O triângulo tem 7,00 m de base por 7,00 m de altura, com a frente toda em vidro voltada para a piscina. No térreo ficam sala, cozinha, lavanderia e banheiro. No pavimento superior, a suíte.',
                'Paredes e laje são em light steel frame. A piscina e a área da churrasqueira seguem em concreto armado.'],
          sections=[
           dict(label='Fachadas',items=[
            I('20-render.jpg',('Frente','vidro do piso à cumeeira'),'Frente da cabana: empena de vidro com a escada e o mezanino à vista, piscina em primeiro plano','full',pos='50% 45%'),
            I('22-render.jpg',('Fundos e lateral','cobertura metálica e volume de dois pavimentos'),'Vista de três quartos pelos fundos, com a água da cobertura metálica e o volume revestido em pedra',r='16/9'),
            I('23-render.jpg',('Fundos','sacada da suíte'),'Fundos da cabana, com a sacada do pavimento superior e o volume de dois pavimentos',r='16/9')]),
           dict(label='Interiores',items=[
            I('24-render.jpg',('Sala','escada e vista para a piscina'),'Sala com a escada de madeira e a frente de vidro aberta para a piscina'),
            I('25-render.jpg',('Frente de vidro','estar sob o mezanino'),'Interior visto da varanda da frente, com estar, escada e mezanino',r='16/9')])])
# Casa do Bosque: modelo de casa de alto padrão (imagens do post do cliente, uso autorizado por ele em nov/2026).
# É MODELO, não obra: as imagens foram geradas por IA e não há projeto técnico por trás. Nunca rotular como obra entregue
# nem como "Etapa: Projeto". Só a fachada de dia entra (a de noite muda pedra, porta e piso); a TV do cinema imita logotipo de estúdio: não usar.
PROJECTS.insert(1,
 dict(slug='casa-do-bosque',name='Casa do Bosque',cat='casa',cat_label='casas',cat_plural='casas',city='modelo',sub='casa de alto padrão · 450 m²',ref='a Casa do Bosque',
  card=dict(src=C+'02-fachada-dia.jpg',focus=(.5,.38),alt='Fachada da Casa do Bosque: laje em balanço, pedra clara e madeira, com espelho d\'água e jardim'),
  hero=dict(src=C+'02-fachada-dia.jpg',pair=C+'03-living.jpg',alt='Fachada da Casa do Bosque: laje em balanço, pedra clara e madeira, com degraus sobre o espelho d\'água',
            alt2='Living com forro de madeira e vidro do piso ao teto, aberto para a piscina e o jardim'),
  lead='Pé-direito amplo, integração com o jardim e <b>pedra, madeira e concreto.</b>',
  text=[],
  ficha=[('Tipo','Casa de alto padrão'),('Área','450 m²'),('Etapa','Modelo · 2026')],
  desc='Casa do Bosque: modelo de casa de alto padrão, 450 m². Luis Gustavo Maia, engenheiro civil.',
  sections=[dict(label='Interiores',items=[
    I('04-suite.jpg',('Suíte',''),'Suíte com forro e painel de madeira, aberta para o terraço',r='4/5'),
    I('05-banho.jpg',('Banho',''),'Banho com banheira de imersão, bancada em pedra e vista para as árvores',r='4/5')])]))
PROJECTS.append(
 dict(slug='casa-da-raia',assets='residencia-ym',name='Casa da Raia',cat='casa',cat_label='casas',cat_plural='casas',city='Marília, SP',sub='casa térrea · 185 m²',ref='a Casa da Raia',
  # Conferência (nov/2026): 14 das 15 vistas seguem plantas, cortes e fachadas. Recortes tiram a casca da piscina que aparece por baixo do muro
  # (o modelo não tem terreno). A casa é de alvenaria; em steel frame, só as treliças do telhado. A arquitetura é de arquiteto parceiro.
  # capa: render no Cycles do modelo montado com as cotas do executivo, conferido em vista ortogonal contra a Fachada Posterior
  card=dict(src='render/01-fachada-fundos-render.png',focus=(.55,.55),alt='Casa da Raia: fachada dos fundos com a porta de correr do estar, a piscina em raia e a cerca viva'),
  hero=dict(src='render/01-fachada-fundos-render.png',pos='50% 55%',alt='Fachada dos fundos da Casa da Raia: telhado cerâmico de duas águas, torre da caixa-d\'água, porta de correr de quatro folhas e a piscina em raia de 18 m'),
  lead='Casa térrea de duas águas, <b>com uma raia de 18 m ao longo do lote.</b>',
  text=[],
  ficha=[('Local','Marília, SP'),('Área','184,60 m²'),('Sistema','Alvenaria, com telhado sobre treliças em steel frame'),('Escopo','Projeto executivo em BIM, sobre arquitetura de arquiteto parceiro'),('Etapa','Projeto · 2026')],
  sections=[]))

# ---- Ajustes da conferência de imagens (nov/2026). Regra do cliente: a imagem tem de ser real e seguir o projeto. ----
def _item(p,prefixo):
    return next(it for sec in p['sections'] for it in sec['items'] if it['src'].split('/')[-1].startswith(prefixo))
for _p in PROJECTS:
    _s=_p['slug']
    if _s=='casa-taquaracu':
        # A aérea da capa e a vista com a edícula saíram: a IA trocou a edícula de lugar (mesa do gourmet, vão vazado, bancada de bar
        # onde a planta tem banheiro) e embaralhou corrimãos. Fica o lado esquerdo da imagem 13 (casa, varanda, escada e piscina),
        # que confere com a planta, em par com o estar. Da cozinha sai a faixa da porta, onde a vista de fora não batia.
        _p.update(card=dict(src=C+'13-ficha.jpg',crop=(0,0,.47,1),focus=(.5,.40),alt='Casa Taquaraçu: varanda sobre pilares e piscina, com a serra ao fundo'),
                  hero=dict(src=C+'13-ficha.jpg',crop=(0,0,.47,1),focus=(.5,.40),pair=C+'04-estar-e-jantar.jpg',pair_focus=(.5,.5),
                            alt='A casa vista da piscina: varanda sobre pilares, escada e telhado de uma água, com a serra ao fundo',
                            alt2='Estar e jantar integrados, com a porta de correr para a varanda'))
        _item(_p,'05-')['crop']=(.125,0,1,1)
    elif _s=='chale-acolher':
        # As duas externas com acabamento por IA contradiziam o projeto (vãos da lateral, lavanderia, caixa-d'água, cor do telhado).
        # Entram os renders diretos do modelo.
        _p.update(card=dict(src=C+'03-render-fachada-frontal-lateral.jpg',fam='d',focus=(.5,.5),alt='Chalé de duas águas revestido em chapa nervurada, render do modelo'),
                  hero=dict(src=C+'03-render-fachada-frontal-lateral.jpg',fam='d',pos='50% 50%',alt='Chalé de duas águas revestido em chapa nervurada, com a porta de correr no oitão dos fundos'))
    elif _s=='chale-piedade':
        # A capa antiga mostrava o deck com o dobro da largura do quadro de áreas e plantas saindo das tábuas. Fica a frontal, que confere.
        _p.update(card=dict(src=C+'01-fachada-norte-hora-azul.jpg',focus=(.5,.5),alt='Cabana A-frame com a empena de vidro acesa ao anoitecer'),
                  hero=dict(src=C+'01-fachada-norte-hora-azul.jpg',pos='50% 55%',alt='Empena de vidro do A-frame ao anoitecer, com o interior aceso e o mezanino ao fundo'))
    elif _s=='tiny-house':
        # Na capa antiga a janela do banho saía com caixilho branco; o projeto pede preto em todas as esquadrias.
        _p.update(card=dict(src=C+'01-fachada-frontal-hora-azul.jpg',focus=(.5,.5),alt='Tiny house de duas águas com a frente de vidro acesa ao anoitecer'),
                  hero=dict(src=C+'01-fachada-frontal-hora-azul.jpg',pos='50% 55%',alt='Frente de vidro da tiny house ao anoitecer, com o loft ao fundo'))
    elif _s=='patio-escolar':
        for _k in ('02-','04-'): _item(_p,_k)['crop']=(0,0,1,.92)
    elif _s=='casa-do-bosque':
        # Suíte e banho mostravam sacada e vista por cima das copas; a fachada é térrea. Fica só o par da capa, que fecha entre si.
        _p['sections']=[]
# Prédio comercial em Garça (pedido do cliente, nov/2026). Nome público sem o nome da empresa.
# A capa é render feito no Cycles (Blender) a partir de um modelo montado só com as medidas da Fachada 04 da prancha aprovada:
# vidro 29,25 x 5,00 m em três vãos, painel de alumínio de 2,00 m, caixa-d'água, muros de divisa. Sem logotipo, sem carros,
# sem vizinhos inventados. As fachadas "realistas" do Drive (Gemini e ChatGPT) redesenham o prédio: não usar.
PROJECTS.append(
 dict(slug='comercial-garca',name='Prédio comercial em Garça',cat='comercial',cat_label='comerciais',cat_plural='comerciais',city='Garça, SP',sub='steel frame · 742 m²',ref='o prédio comercial de Garça',
  card=dict(src=C+'02-fachada-render.png',crop=(0,.04,1,.96),focus=(.5,.62),alt='Fachada do prédio comercial: salão com frente de vidro de 29 m e painel de alumínio, render do projeto'),
  hero=dict(src=C+'02-fachada-render.png',pos='50% 60%',alt='Fachada do prédio comercial em Garça vista da rua: frente de vidro em três vãos com porta dupla central e painel de alumínio, render do projeto aprovado'),
  lead='Salão com 29 m de frente em vidro, <b>estrutura em steel frame.</b>',
  text=[],
  ficha=[('Local','Garça, SP'),('Área','741,69 m²'),('Sistema','Light steel frame'),('Escopo','Projeto arquitetônico e legal, estrutura em steel frame e CNO'),('Etapa','Projeto aprovado · 2026')],
  sections=[]))
# Casa Garça (pedido do cliente, nov/2026; nome público sem nome de cliente). A única fachada "renderizada" do Drive é de IA (GPT-4o)
# e junta os portões, apaga os muros e inventa serra e vizinho: não usar. A capa é render no Cycles de um modelo montado só com as
# cotas da Fachada Norte, do Detalhe da Fachada, da Planta de Cobertura e do Corte A-A (site-build/render/casagarca_blender.py),
# conferido em vista ortogonal contra a Fachada Norte. Cores neutras: as pranchas não definem acabamento.
PROJECTS.append(
 dict(slug='casa-garca',assets='casa-garca',name='Casa Garça',cat='casa',cat_label='casas',cat_plural='casas',city='Garça, SP',sub='casa térrea · 135 m²',ref='a Casa Garça',
  card=dict(src='render/01-fachada-render.png',focus=(.5,.6),alt='Casa Garça: fachada com portão basculante, portão social, tabeira metálica e volumes com platibanda'),
  hero=dict(src='render/01-fachada-render.png',pos='50% 60%',alt='Fachada da Casa Garça vista da rua: muro com portão basculante e portão social, tabeira metálica sobre a garagem e os volumes da casa com platibanda'),
  lead='Casa térrea em terreno de 10 m de frente, <b>com garagem para dois carros sob a tabeira.</b>',
  text=[],
  ficha=[('Local','Garça, SP'),('Área','135,26 m², em terreno de 200 m²'),('Sistema','Alvenaria, cobertura metálica com telha sanduíche'),('Escopo','Projeto executivo e projeto legal'),('Etapa','Projeto · 2025')],
  sections=[]))
# ---- Regra de capa (nov/2026): a obra abre com UMA fachada renderizada; internas e estrutura vêm dentro da página. ----
for _p in PROJECTS:
    _s=_p['slug']
    if _s=='salas-comerciais':
        _p.update(card=dict(src=C+'01-fachada-rua.jpg',crop=(0,.56,1,1),focus=(.42,.5),alt='Fachada das salas comerciais vista da rua, com muro verde e painéis de cobogó'),
                  hero=dict(src=C+'01-fachada-rua.jpg',crop=(0,.56,1,1),pos='50% 50%',alt='Fachada das salas comerciais vista da rua, com muro verde, cobogó e portão branco'))
    elif _s=='casa-taquaracu':
        _h=_p['hero']; _p['hero']=dict(src=_h['src'],crop=_h.get('crop'),pos='50% 40%',alt=_h['alt'])
    elif _s=='casa-do-bosque':
        _h=_p['hero']; _p['hero']=dict(src=_h['src'],pos='50% 40%',alt=_h['alt'])
        _p['sections']=[dict(label='Interiores',items=[I('03-living.jpg',('Living',''),'Living com forro de madeira e vidro do piso ao teto, aberto para a piscina e o jardim','full')])]
PROJECTS_FULL=PROJECTS
PROJECTS=_lean(PROJECTS)
# ordem das obras (grade 2 · 3 · 3 · 3 · 2): steel frame de alto padrão e obra concluída primeiro; desenhos e estruturas no fim
# Residência em concreto armado (Marília): pedido do cliente (nov/2026) "mostre apenas projeto estrutural e complementares, o
# arquitetônico não é do nosso escritório". Capa = 3D da estrutura do modelo TQS (sem IA, sem arquitetura). Nome público neutro.
PROJECTS.append(
 dict(slug='residencia-concreto',assets='obra-concreto',name='Residência em concreto armado',cat='estrutura',cat_label='estruturas',cat_plural='estruturas',city='Marília, SP',sub='concreto armado · 97 m²',ref='a residência em concreto armado',
  card=dict(src=C+'estrutura-01-tres-quartos.jpg',focus=(.5,.5),fam='c',alt='Estrutura em concreto armado de uma residência térrea: pilares, vigas e lajes do modelo estrutural'),
  hero=dict(src=C+'estrutura-01-tres-quartos.jpg',draw='night',fam='c',alt='Modelo estrutural em concreto armado de uma residência térrea, com pilares, vigas e lajes técnicas da caixa-d\'água'),
  lead='Estrutura e complementares de uma casa térrea, <b>com a obra em andamento.</b>',
  text=[],
  ficha=[('Local','Marília, SP'),('Área','97,19 m²'),('Sistema','Concreto armado com laje treliçada'),('Escopo','Projeto estrutural e projetos complementares'),('Etapa','Obra em andamento · 2026')],
  sections=[dict(label='Estrutura',items=[I('estrutura-02-fundos.jpg',('Estrutura vista pelos fundos',''),'Modelo estrutural em concreto armado visto pelos fundos, com pilares, vigas e lajes','full')])]))
FAM['obra-concreto']={'estrutura-01-tres-quartos.jpg':'c','estrutura-02-fundos.jpg':'c'}
# Casa Duo (v37): imagens renderizadas que o escritório entregou na prancha do projeto simplificado (fachada, entrada, área
# externa, sala), no padrão de produto pronto da Casa do Bosque. Número da casa apagado da fachada (endereço). Planta e
# carimbo da prancha não entram.
for _p in PROJECTS:
    if _p['slug']=='casa-duo':
        _p.update(card=dict(src='render/01-fachada.png',focus=(.5,.45),alt='Casa Duo ao anoitecer: muro em pedra com iluminação de jardim, porta de vidro e portão da garagem sob a laje'),
          hero=dict(src='render/01-fachada.png',pos='50% 40%',alt='Fachada da Casa Duo ao anoitecer, com muro revestido, porta de vidro, portão da garagem e a laje da casa ao fundo'),
          lead='Casa térrea em dois lotes unidos, <b>com piscina e garagem para dois carros.</b>',
          text=[],
          sections=[dict(label='Externas',items=[
             I('../render/02-entrada.png',('Entrada',''),'Entrada coberta com forro de madeira, porta pivotante preta e janela com cortina','half'),
             I('../render/03-area-externa.png',('Área externa',''),'Piscina com deck de madeira, jardim vertical e espreguiçadeiras','half')]),
           dict(label='Interiores',items=[I('../render/04-sala.png',('Sala',''),'Sala com painel ripado, rack de madeira e sofá em L','full')])])
# ---- Fichas no padrão de cinco linhas (conferência de nov/2026). Ano só onde está no arquivo do projeto. ----
for _p in PROJECTS:
    if _p['slug']=='chale-piedade':
        _p['ficha']=[('Local','Piedade, SP'),('Área','70,35 m²'),('Sistema','A-frame com mezanino em light steel frame'),('Escopo','Projeto de arquitetura'),('Etapa','Projeto · 2024')]
    if _p['slug']=='tiny-house':
        _p['ficha']=[('Local','Sorocaba, SP'),('Área','38,57 m²'),('Sistema','Fechamento em telha metálica de junta elevada'),('Escopo','Projeto de arquitetura'),('Etapa','Projeto · 2024')]
    if _p['slug']=='casa-do-bosque':
        _p['ficha']=[('Local','Modelo, sem terreno definido'),('Área','450 m²'),('Sistema','A definir no projeto'),('Escopo','Modelo de casa de alto padrão'),('Etapa','Modelo · 2026')]
FICHA_KEEP['chale-piedade']=FICHA_KEEP['tiny-house']=['Local','Área','Sistema','Escopo','Etapa']
FICHA_KEEP.pop('casa-do-bosque',None)
ORDEM=['casa-taquaracu','salas-comerciais','comercial-garca','casa-garca','chale-piedade','chale-viver','tiny-house','chale-acolher','chale-analandia','casa-do-bosque',
       'casa-da-raia','casa-duo','residencia-concreto','patio-escolar','ampliacao-steel-frame','le-blanc-lofts']
ORDEM=[k for k in ORDEM if k not in HELD]
assert sorted(ORDEM)==sorted(p['slug'] for p in PROJECTS),sorted(set(ORDEM)^set(p['slug'] for p in PROJECTS))
PROJECTS.sort(key=lambda p: ORDEM.index(p['slug']))
OBRAS_META='casas, chalés, salas comerciais e estruturas em aço'
