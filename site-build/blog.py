# -*- coding: utf-8 -*-
# Blog do site L. Engenharia.
# REGRA EDITORIAL (instrução direta do cliente, nov/2026): texto básico, direto e reto. Quem é referência
# segura o conhecimento e fala o básico: o leitor entende que existe o caminho e procura o engenheiro para
# saber como. Nada de passo a passo, tabela de percentuais, lista de documentos ou memória de cálculo.
# Fonte: só o título, sem link e sem PDF.
# Só entra afirmação conferida em fonte primária (a versão longa e conferida está em blog.py.bak-v19-longo).
# Corpo = lista de (rótulo da margem, html). Ordem: primeiro a parte tributária, depois steel frame.

DATA = 'atualizado em novembro de 2026'
INDEX_H1 = 'Perguntas de quem vai construir, <b>respondidas direto ao ponto.</b>'
INDEX_LEAD = 'O imposto da obra, em primeiro lugar. Depois, steel frame. <b>Um minuto cada.</b>'
HOME = ['steel-frame-paga-menos-inss', 'cno-prazo-e-inscricao', 'obra-antiga-decadencia']

# fontes: só o título
F_IN2021 = 'Instrução Normativa RFB nº 2.021, de 2021'
F_IN2061 = 'Instrução Normativa RFB nº 2.061, de 2021'
F_MANUAL = 'Manual do Sero, Receita Federal'
F_CTN = 'Código Tributário Nacional, art. 173'
F_DATEC = 'Documento de Avaliação Técnica nº 14, SINAT, com avaliação do IPT'
# Os estudos de caso de custo (PUC Goiás, Unipar e Ceulp/Ulbra) nunca foram abertos: não entram como fonte até serem lidos.

def P(*ps): return ''.join('<p>%s</p>' % p for p in ps)

ARTICLES = [

dict(slug='steel-frame-paga-menos-inss', cover=dict(src='chale-acolher/clean/03-render-fachada-frontal-lateral.jpg',fam='d',focus=(.5,.5),alt='Chalé Acolher em steel frame: fachada de duas águas revestida em chapa nervurada',cap=('Chalé Acolher','steel frame · Marília, SP')),
 tema='imposto', mins=1,
 title='Steel frame paga menos INSS?',
 h1='Steel frame paga menos INSS? <b>Pode pagar.</b>',
 lead='A norma da Receita não cita steel frame. Fala em estrutura de metal e em pré-fabricado. <b>A casa em steel frame pode caber nas duas descrições.</b>',
 resumo='A norma não cita o sistema, mas descreve o que ele é.',
 desc='Steel frame paga menos INSS de obra? Pode pagar: a norma da Receita Federal trata estrutura de metal e pré-fabricado de forma diferente da alvenaria.',
 body=[
  ('Resposta curta', P('Paga menos quando a obra é inscrita do jeito certo e as notas fiscais sustentam o enquadramento. <b>Sem isso, a Receita calcula a casa em steel frame como alvenaria.</b>')),
  ('O que muda', P('No enquadramento certo, a base do imposto é menor. A diferença pode chegar a 70%.')),
  ('O ponto de atenção', P('Nada é automático. <b>O enquadramento é decidido antes da compra do aço</b> e conferido obra a obra.')),
 ],
 fontes=[F_IN2021, F_MANUAL], rel=['fator-de-ajuste','cno-prazo-e-inscricao'], call='Vai construir em steel frame?'),

dict(slug='cno-prazo-e-inscricao', cover=dict(src='tiny-house/clean/01-fachada-frontal-hora-azul.jpg',focus=(.5,.55),alt='Tiny House de duas águas com a frente de vidro acesa ao anoitecer',cap=('Tiny House','Sorocaba, SP')),
 tema='imposto', mins=1,
 title='CNO: quem inscreve a obra e em que prazo',
 h1='CNO: quem inscreve a obra e em que prazo. <b>O responsável, em até 30 dias.</b>',
 lead='O Cadastro Nacional de Obras é o registro da construção na Receita Federal. <b>O que é declarado ali define o INSS no fim.</b>',
 resumo='O prazo de 30 dias e por que a inscrição define o imposto.',
 desc='CNO, o Cadastro Nacional de Obras: quem inscreve a obra, o prazo de 30 dias e por que a inscrição define o INSS.',
 body=[
  ('Resposta curta', P('A obra é inscrita no CNO em até 30 dias do início. <b>Quem inscreve é o responsável pela obra:</b> o proprietário, o dono da obra ou a construtora, na empreitada total.')),
  ('Por que importa', P('Categoria, tipo, área e destinação são informados na inscrição. <b>São esses campos que alimentam o cálculo do imposto.</b>')),
  ('O erro comum', P('Tratar a inscrição como formalidade. Perder o prazo sujeita o responsável a multa, e o que foi informado segue para o cálculo.')),
 ],
 fontes=[F_IN2061, F_IN2021], rel=['steel-frame-paga-menos-inss','obra-antiga-decadencia'], call='Vai começar uma obra?'),

dict(slug='obra-antiga-decadencia', cover=dict(src='chale-viver/clean/04-render-fachada-frontal.jpg',focus=(.5,.6),alt='Chalé Viver: casa térrea com a garagem sob pergolado metálico preto',cap=('Chalé Viver','Marília, SP')),
 tema='imposto', mins=1,
 title='Construí há mais de cinco anos. Ainda devo INSS?',
 h1='Construí há mais de cinco anos. Ainda devo INSS? <b>Depende da data.</b>',
 lead='É a decadência: passado o prazo, a Receita não cobra mais. <b>O prazo corre a favor de quem construiu, mas a prova é dele.</b>',
 resumo='O prazo existe. O que decide é a prova da data.',
 desc='Decadência no INSS de obra: quando a construção com mais de cinco anos não paga contribuição e por que a prova da data decide.',
 body=[
  ('Resposta curta', P('A Receita tem cinco anos para lançar a contribuição, contados do primeiro dia do ano seguinte. <b>Passado o prazo, a obra é regularizada sem contribuição a recolher, desde que a data seja provada.</b>')),
  ('O que decide', P('O documento. Vale o que liga a construção à data, e precisa ser da época.')),
  ('Atenção', P('A regularização continua necessária para tirar a certidão da obra. <b>E quando só uma parte é antiga, o imposto incide sobre o resto.</b>')),
 ],
 fontes=[F_IN2021, F_CTN, F_MANUAL], rel=['cno-prazo-e-inscricao','fator-de-ajuste'], call='Tem uma construção antiga para regularizar?'),

dict(slug='fator-de-ajuste', cover=dict(src='chale-piedade/clean/01-fachada-norte-hora-azul.jpg',focus=(.5,.55),alt='Chalé Piedade: cabana A-frame com a empena de vidro acesa ao anoitecer',cap=('Chalé Piedade','Piedade, SP')),
 tema='imposto', mins=1,
 title='Fator de ajuste: quando a aferição fecha em zero',
 h1='Fator de ajuste: <b>quem declarou a mão de obra pode fechar a aferição em zero.</b>',
 lead='Para a pessoa física que construiu com mão de obra declarada, a norma tem uma regra de fechamento. <b>Atingido o mínimo, com declaração em todos os meses, a aferição termina sem contribuição a recolher.</b>',
 resumo='A regra que fecha a aferição sem débito para quem declarou a mão de obra.',
 desc='Fator de ajuste no INSS de obra: quando a pessoa física que declarou a mão de obra fecha a aferição sem contribuição a recolher.',
 body=[
  ('Resposta curta', P('Quem declara a mão de obra durante a obra, mês a mês, pode fechar a aferição sem débito. <b>A regra vale para pessoa física e tem um mínimo a atingir.</b>')),
  ('Onde falha', P('Um mês sem declaração derruba a regra. Remuneração sem vínculo com a obra não conta.')),
  ('Na prática', P('<b>É decisão de começo de obra:</b> a declaração precisa cobrir todos os meses.')),
 ],
 fontes=[F_IN2021, F_MANUAL], rel=['steel-frame-paga-menos-inss','cno-prazo-e-inscricao'], call='Quer a obra declarada do jeito certo?'),

dict(slug='steel-frame-e-mais-caro', cover=dict(src='chale-analandia/clean/21-render.jpg',crop=(0,0,.9,1),focus=(.4,.5),alt='Chalé Analândia: cabana A-frame em steel frame, com piscina e churrasqueira',cap=('Chalé Analândia','steel frame · Analândia, SP')),
 tema='steel frame', mins=1,
 title='Steel frame é mais caro?',
 h1='Steel frame é mais caro? <b>Depende da conta.</b>',
 lead='Na planilha, costuma ser. Quem compara só o custo direto costuma parar na alvenaria. <b>Prazo, repetição e imposto mudam o resultado.</b>',
 resumo='O que a planilha mostra e o que ela deixa de fora.',
 desc='Steel frame é mais caro que alvenaria? No custo direto, costuma ser. Prazo, repetição e INSS de obra mudam a conta.',
 body=[
  ('Resposta curta', P('No custo direto, o steel frame costuma sair acima da alvenaria. <b>A diferença cai, e pode se inverter, quando entram o prazo de obra, a repetição do projeto e o INSS.</b>')),
  ('O que fica fora da planilha', P('Obra mais curta custa menos em canteiro e em aluguel. Projeto resolvido no desenho vira previsibilidade. <b>E o imposto da obra costuma ficar fora da comparação.</b>')),
  ('Como comparar', P('Compare a casa pronta, com o mesmo acabamento, o prazo em reais e o INSS nos dois cenários.')),
 ],
 fontes=[F_IN2021], rel=['steel-frame-paga-menos-inss','steel-frame-conforto-termoacustico'], call='Quer a conta inteira do seu projeto?'),

dict(slug='steel-frame-conforto-termoacustico', cover=dict(src='chale-acolher/clean/04-render-lateral-direita-lavanderia.jpg',fam='d',focus=(.5,.5),alt='Chalé Acolher em steel frame visto pela lateral',cap=('Chalé Acolher','steel frame · Marília, SP')),
 tema='steel frame', mins=1,
 title='Steel frame tem melhor conforto termoacústico?',
 h1='Steel frame tem melhor conforto termoacústico? <b>Quem responde é a parede.</b>',
 lead='A parede de steel frame é um conjunto de camadas. <b>No som, o resultado de laboratório passa com folga do mínimo. No calor, depende do projeto.</b>',
 resumo='No som, a parede ensaiada passou com folga. No calor, depende do projeto.',
 desc='Conforto térmico e acústico do steel frame: o que ensaio de laboratório mediu no isolamento de som e por que o desempenho térmico depende do projeto.',
 body=[
  ('Som', P('Em ensaio de laboratório, uma parede de fachada com lã de vidro no miolo, sem janela, isolou 50 dB. <b>O mínimo da avaliação era 30 dB.</b>')),
  ('Calor', P('Isolante, cor da fachada, sombra e ventilação decidem se a casa atende.')),
  ('O que isso quer dizer', P('Steel frame não é mais nem menos confortável por ser steel frame. <b>Conforto se especifica no projeto.</b>')),
 ],
 fontes=[F_DATEC], rel=['steel-frame-e-mais-caro','steel-frame-paga-menos-inss'], call='Vai construir em steel frame?'),
]
