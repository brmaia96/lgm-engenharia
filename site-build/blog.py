# -*- coding: utf-8 -*-
# Blog do site L. Engenharia.
# REGRA EDITORIAL (instrução direta do cliente, nov/2026): texto básico, direto e reto. Quem é referência
# segura o conhecimento e fala o básico: o leitor entende que existe o caminho e procura o engenheiro para
# saber como. Nada de passo a passo, tabela de percentuais, lista de documentos ou memória de cálculo.
# Fonte: só o título, sem link e sem PDF.
# Só entra afirmação conferida em fonte primária (a versão longa e conferida está em blog.py.bak-v19-longo).
# Corpo = lista de (rótulo da margem, html). Ordem: primeiro a parte tributária, depois steel frame.

DATA = 'atualizado em novembro de 2026'
INDEX_H1 = 'O que pesa na obra <b>antes do primeiro tijolo.</b>'
INDEX_LEAD = 'O imposto da obra em primeiro lugar, depois o steel frame. <b>Textos curtos, com o que a norma diz e o que costuma custar caro.</b>'
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

dict(slug='steel-frame-paga-menos-inss', cover=dict(src='chale-acolher/clean/06-render-estrutura-lsf.jpg',fam='c',focus=(.5,.5),alt='Estrutura completa em steel frame de um chalé: painéis de parede, tesouras e cobertura em aço galvanizado',cap=('Estrutura em steel frame','Chalé Acolher · Marília, SP')),
 tema='imposto', mins=2,
 title='Steel frame paga menos INSS?',
 h1='Steel frame paga menos INSS? <b>Pode pagar, se a obra for tratada como o que ela é.</b>',
 lead='A norma da Receita não usa a palavra steel frame. Ela fala em estrutura de metal e em construção pré-fabricada. <b>É nesse texto que está a diferença no imposto.</b>',
 resumo='A norma não cita o sistema, mas descreve exatamente o que ele é.',
 desc='Steel frame paga menos INSS de obra? Pode pagar: a norma da Receita Federal trata estrutura de metal e pré-fabricado de forma diferente da alvenaria.',
 body=[
  ('O que a norma diz', P('O INSS de uma obra de pessoa física não é calculado sobre o que se gastou de fato. A Receita parte da área construída e de um custo padrão por metro quadrado, publicado mês a mês para cada estado, e presume quanto daquilo foi mão de obra. <b>A presunção muda conforme o tipo de construção.</b>',
    'A Instrução Normativa que rege o assunto separa a alvenaria das obras com estrutura de metal e das pré-fabricadas. Ela não cita steel frame em nenhuma linha, mas descreve o sistema com precisão. Quem conhece o texto sabe enquadrar a obra; quem não conhece paga como se a casa fosse de tijolo.')),
  ('Onde se perde dinheiro', P('O erro mais caro é o silencioso: a casa é construída em aço, mas é inscrita e aferida como alvenaria, porque ninguém levou o sistema construtivo para dentro do processo. <b>A redução prevista pode chegar a 70% da base do imposto</b>, e ela simplesmente não acontece.',
    'O enquadramento não se pede no fim. Ele depende de como a obra foi inscrita, de como foi comprada e de como foi documentada desde o começo.')),
  ('Antes de começar', P('Se a casa vai ser em steel frame, a conversa sobre o INSS vem antes da compra do aço. <b>Cada obra é conferida no seu caso</b>, contra a norma e contra o que a Receita vai pedir na aferição.')),
 ],
 fontes=[F_IN2021, F_MANUAL], rel=['fator-de-ajuste','cno-prazo-e-inscricao'], call='Vai construir em steel frame?'),

dict(slug='cno-prazo-e-inscricao', cover=dict(src='blog-art/cno-prazo-e-inscricao.png',fam='x',focus=(.5,.5),alt='Ilustração: a ficha de inscrição da obra no Cadastro Nacional de Obras e o prazo de 30 dias'),
 tema='imposto', mins=2,
 title='CNO: quem inscreve a obra e em que prazo',
 h1='CNO: quem inscreve a obra e em que prazo. <b>O responsável, em até 30 dias do início.</b>',
 lead='O Cadastro Nacional de Obras é a certidão de nascimento da construção na Receita Federal. <b>Tudo o que vem depois, inclusive o INSS, parte do que foi declarado ali.</b>',
 resumo='O prazo de 30 dias e por que a inscrição já decide o imposto.',
 desc='CNO, o Cadastro Nacional de Obras: quem inscreve a obra, o prazo de 30 dias e por que a inscrição define o INSS.',
 body=[
  ('Quem e quando', P('A inscrição é obrigação do responsável pela obra: o proprietário ou dono da obra, ou a construtora, quando a contratação é por empreitada total. <b>O prazo é de 30 dias contados do início da obra.</b>',
    'Perdido o prazo, o responsável fica sujeito a multa. Mas a multa é o menor dos problemas.')),
  ('Por que importa', P('Na inscrição se informam a categoria da obra, o tipo de construção, a área e a destinação. <b>Esses campos alimentam diretamente o cálculo do imposto no fim da obra.</b> Uma informação lançada de forma apressada no primeiro mês acompanha a obra até a aferição.',
    'É comum ver o CNO tratado como formalidade, feito por quem não vai acompanhar a obra. É exatamente aí que a conta começa a sair mais alta do que precisava.')),
  ('Antes de começar', P('A inscrição é a primeira decisão tributária da obra, não a última. <b>Feita com o projeto em mãos</b>, ela já nasce coerente com o que a obra vai ser.')),
 ],
 fontes=[F_IN2061, F_IN2021], rel=['steel-frame-paga-menos-inss','obra-antiga-decadencia'], call='Vai começar uma obra?'),

dict(slug='obra-antiga-decadencia', cover=dict(src='blog-art/obra-antiga-decadencia.png',fam='x',focus=(.5,.5),alt='Ilustração: linha do tempo de cinco anos contados a partir de 1º de janeiro do ano seguinte'),
 tema='imposto', mins=2,
 title='Construí há mais de cinco anos. Ainda devo INSS?',
 h1='Construí há mais de cinco anos. Ainda devo INSS? <b>Talvez não. Depende do que você consegue provar.</b>',
 lead='A lei dá à Receita um prazo para cobrar. Passado esse prazo, o direito de lançar a contribuição acaba. <b>É a decadência, e ela corre a favor de quem construiu.</b>',
 resumo='O prazo existe. O que decide é a prova da data.',
 desc='Decadência no INSS de obra: quando a construção com mais de cinco anos não paga contribuição e por que a prova da data decide.',
 body=[
  ('O que diz a lei', P('O prazo é de cinco anos, contados a partir do primeiro dia do ano seguinte ao da ocorrência. <b>Uma construção comprovadamente concluída dentro do período já vencido é regularizada sem contribuição a recolher.</b>',
    'Na prática, isso significa que muita casa antiga que nunca foi averbada pode ser regularizada sem o imposto que o proprietário imagina dever.')),
  ('O que decide', P('A data não se declara, se prova. <b>Vale o documento da época que liga aquela construção àquele ano</b>, e é ele que a Receita examina.',
    'Quando a casa recebeu ampliação recente, a conta muda: a parte antiga pode estar fora do prazo e a parte nova, não. Cada metro quadrado tem a sua data.')),
  ('Antes de regularizar', P('A regularização continua necessária para obter a certidão da obra. <b>O que muda é quanto ela custa</b>, e isso se decide no levantamento da prova, antes de qualquer declaração.')),
 ],
 fontes=[F_IN2021, F_CTN, F_MANUAL], rel=['cno-prazo-e-inscricao','fator-de-ajuste'], call='Tem uma construção antiga para regularizar?'),

dict(slug='fator-de-ajuste', cover=dict(src='blog-art/fator-de-ajuste.png',fam='x',focus=(.5,.5),alt='Ilustração: balança entre o que a Receita presume e o que a obra declarou'),
 tema='imposto', mins=2,
 title='Fator de ajuste: quando a aferição fecha em zero',
 h1='Fator de ajuste: <b>a regra que pode fechar a aferição da obra sem débito.</b>',
 lead='Para a pessoa física que construiu com mão de obra registrada, a norma tem uma regra de fechamento. <b>Cumprida a condição, a aferição termina sem contribuição a recolher.</b>',
 resumo='A regra que fecha a aferição sem débito para quem declarou a mão de obra.',
 desc='Fator de ajuste no INSS de obra: quando a pessoa física que declarou a mão de obra fecha a aferição sem contribuição a recolher.',
 body=[
  ('O que é', P('No fim da obra, a Receita compara o que ela presume de mão de obra com o que foi efetivamente declarado durante a construção. <b>O fator de ajuste é a regra que, atingido um mínimo declarado, zera a diferença.</b>',
    'Nas aferições que acompanhamos, é ele que transforma débitos de milhares de reais em zero, dentro da norma e com documento da própria Receita.')),
  ('Onde falha', P('A regra exige constância. <b>Um único mês sem declaração derruba o benefício</b>, e remuneração que não está vinculada à obra não conta.',
    'Por isso ela quase nunca funciona quando é lembrada só no fim. Quem descobre o fator de ajuste na hora da aferição normalmente já o perdeu.')),
  ('Antes de começar', P('O fator de ajuste é decisão de primeiro mês de obra. <b>Planejado desde o início</b>, ele costuma decidir o resultado da obra de pessoa física.')),
 ],
 fontes=[F_IN2021, F_MANUAL], rel=['steel-frame-paga-menos-inss','cno-prazo-e-inscricao'], call='Quer a obra declarada do jeito certo?'),

dict(slug='steel-frame-e-mais-caro', cover=dict(src='taquaracu/clean/08-fundacao-e-estrutura.jpg',fam='c',focus=(.5,.52),alt='Modelo 3D da estrutura em steel frame de uma casa, sobre laje apoiada em pilares',cap=('Estrutura em steel frame','Casa Taquaraçu · Taquaraçu de Minas, MG')),
 tema='steel frame', mins=2,
 title='Steel frame é mais caro?',
 h1='Steel frame é mais caro? <b>Na planilha, às vezes. Na obra pronta, depende da conta.</b>',
 lead='Quem compara só o preço do material costuma voltar para a alvenaria. <b>A comparação honesta é entre duas casas prontas, no mesmo padrão, com tudo o que cada uma custa.</b>',
 resumo='O que a planilha mostra e o que ela deixa de fora.',
 desc='Steel frame é mais caro que alvenaria? No custo direto, costuma ser. Prazo, repetição e INSS de obra mudam a conta.',
 body=[
  ('O que a planilha mostra', P('No custo direto de estrutura e fechamento, o steel frame costuma sair acima da alvenaria. <b>É um número real, mas é só uma parte da conta.</b>')),
  ('O que fica de fora', P('Obra mais curta custa menos: menos meses de canteiro, de equipe, de aluguel enquanto a casa não fica pronta. Projeto resolvido no desenho, com cada peça definida antes de chegar à obra, reduz desperdício e improviso.',
    '<b>E há o imposto da obra, que quase nunca entra na comparação</b> e que, no enquadramento certo, pode pesar a favor do aço.')),
  ('Como comparar', P('Compare a casa entregue, com o mesmo acabamento, o prazo convertido em reais e o INSS calculado nos dois cenários. <b>É essa conta que mostra qual sistema faz sentido para o seu projeto.</b>')),
 ],
 fontes=[F_IN2021], rel=['steel-frame-paga-menos-inss','steel-frame-conforto-termoacustico'], call='Quer a conta inteira do seu projeto?'),

dict(slug='steel-frame-conforto-termoacustico', cover=dict(src='blog-art/steel-frame-conforto-termoacustico.png',fam='x',focus=(.5,.5),alt='Ilustração: corte de uma parede em steel frame com placa externa, membrana, OSB, montante de aço com lã mineral e duas placas de gesso'),
 tema='steel frame', mins=2,
 title='Steel frame tem melhor conforto termoacústico?',
 h1='Steel frame tem melhor conforto termoacústico? <b>Quem responde é a parede, não o sistema.</b>',
 lead='Uma parede de steel frame é um conjunto de camadas, e cada camada tem uma função. <b>No som, o ensaio de laboratório passou com folga do mínimo. No calor, o resultado depende do projeto.</b>',
 resumo='No som, a parede ensaiada passou com folga. No calor, depende do projeto.',
 desc='Conforto térmico e acústico do steel frame: o que ensaio de laboratório mediu no isolamento de som e por que o desempenho térmico depende do projeto.',
 body=[
  ('Som', P('Na avaliação técnica oficial do sistema, uma parede de fachada com lã de vidro no miolo, ensaiada em laboratório sem janela, isolou 50 dB. <b>O mínimo exigido na avaliação era de 30 dB.</b>',
    'O número vale para aquela composição. Trocar o isolante, uma placa ou a vedação das juntas muda o resultado.')),
  ('Calor', P('O desempenho térmico não vem pronto com o aço. <b>Isolante, cor da fachada, sombreamento e ventilação decidem se a casa atende</b> ao clima em que está.')),
  ('O que isso quer dizer', P('Steel frame não é mais nem menos confortável por ser steel frame. <b>Conforto se especifica camada por camada, no projeto</b>, para o terreno e o uso daquela casa.')),
 ],
 fontes=[F_DATEC], rel=['steel-frame-e-mais-caro','steel-frame-paga-menos-inss'], call='Vai construir em steel frame?'),
]
