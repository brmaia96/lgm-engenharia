# -*- coding: utf-8 -*-
# Blog do site L. Engenharia. Cada artigo responde a uma pergunta de quem vai construir, com norma, número e fonte.
# Só entra afirmação conferida em fonte primária. Corpo = lista de (rótulo da margem, html).
# Ordem: primeiro a parte tributária (é o que o escritório domina e o que traz o cliente), depois steel frame.
import importlib.util, os
_s = importlib.util.spec_from_file_location('inss_page', os.path.dirname(os.path.abspath(__file__)) + '/inss_page.py')
N = importlib.util.module_from_spec(_s); _s.loader.exec_module(N)
brl = N.brl

DATA = 'atualizado em novembro de 2026'
INDEX_H1 = 'Perguntas de quem vai construir, <b>respondidas com norma e número.</b>'
INDEX_LEAD = 'O imposto da obra, em primeiro lugar. Depois, custo e conforto do steel frame. <b>Sem promessa: o que a norma diz, o que a conta mostra e onde está a fonte.</b>'
HOME = ['steel-frame-paga-menos-inss', 'cno-prazo-e-inscricao', 'obra-antiga-decadencia']

F_IN2021 = ('Instrução Normativa RFB nº 2.021, de 16 de abril de 2021, texto consolidado.', N.URL_IN2021)
F_IN2061 = ('Instrução Normativa RFB nº 2.061, de 20 de dezembro de 2021. Cadastro Nacional de Obras (CNO).', N.URL_IN2061)
F_MANUAL = ('Receita Federal. Manual do Sero, versão 3.0, agosto de 2024.', N.URL_MANUAL)
F_CTN = ('Código Tributário Nacional, Lei nº 5.172, de 1966, art. 173.', N.URL_CTN)
F_L8212 = ('Lei nº 8.212, de 24 de julho de 1991, arts. 33, 47 e 49.', N.URL_LEI8212)
F_DECAD = ('Receita Federal. Como regularizar uma construção antiga.', 'https://www.gov.br/receitafederal/pt-br/assuntos/construcao-civil/sero/decadencia')

def fig(rows, title, sub, label):
    return ('<figure class="fig" style="margin-top:40px"><div class="bars" role="img" aria-label="%s">%s</div>'
            '<figcaption class="cap"><b>%s</b><span>%s</span></figcaption></figure>') % (label, '\n'.join(rows), title, sub)

CASA = 'casa de %d m² · pessoa física · VAU de referência de %s por m²' % (N.AREA, brl(N.VAU))

ARTICLES = [

dict(slug='steel-frame-paga-menos-inss', tema='imposto', mins=5,
 title='Steel frame paga menos INSS?',
 h1='Steel frame paga menos INSS? <b>Pode pagar, se a obra provar o que é.</b>',
 lead='A norma da Receita não fala em steel frame. Fala em estrutura de metal e em componente pré-fabricado. <b>A casa em steel frame cabe nas duas descrições, e cada uma muda a conta de um jeito.</b>',
 resumo='Tipo misto, pré-fabricado e as notas fiscais que sustentam cada enquadramento.',
 desc='Como a Receita Federal trata a casa em steel frame no INSS de obra: tipo misto, redução de pré-fabricado, notas que contam e o que derruba o enquadramento.',
 body=[
  ('Resposta curta', '<p class="big">Paga menos quando a obra é inscrita com o tipo certo e as notas fiscais sustentam o enquadramento. Sem isso, a Receita calcula a casa em steel frame como alvenaria.</p>'),
  ('A regra', '<p>Sem contabilidade que comprove a mão de obra, a Receita presume o valor pela área. Primeiro apura o custo da obra. Depois aplica um percentual sobre esse custo, que depende do tipo da obra.</p>'
   '<table class="tb"><thead><tr><th scope="col">Tipo da obra</th><th scope="col">Critério</th><th scope="col">Mão de obra presumida</th></tr></thead><tbody>'
   '<tr><th scope="row">Alvenaria</th><td>o que não for madeira nem mista</td><td>20% do custo</td></tr>'
   '<tr><th scope="row">Mista</th><td>paredes externas ou estrutura de madeira, de metal ou pré-fabricadas</td><td>15% do custo</td></tr>'
   '<tr><th scope="row">Madeira</th><td>paredes externas e estrutura de madeira</td><td>15% do custo</td></tr>'
   '</tbody></table>'
   '<p>A classificação olha só para a estrutura e para as paredes externas. Cobertura, alicerce, piso e paredes internas não contam. Laje pré-moldada também não muda o tipo.</p>'),
  ('Dois critérios', '<h3>Estrutura de metal: tipo misto</h3>'
   '<p>No steel frame, a estrutura são os perfis de aço galvanizado. A obra entra no tipo misto e a mão de obra presumida cai de 20% para 15% do custo. A Receita pode pedir o projeto aprovado e a nota fiscal de compra da estrutura.</p>'
   '<h3>Pré-fabricado: redução de 70%</h3>'
   '<p>Quando a estrutura ou as paredes externas são fabricadas por terceiros e montadas na obra, a remuneração apurada tem redução de 70%. A condição é documental: as notas de venda e de instalação ou montagem precisam somar pelo menos 40% do custo da obra calculado pela Receita.</p>'
   '<p>Um ponto do Manual do Sero muda o planejamento. Para ter a redução, a obra é inscrita como alvenaria, porque o cálculo é feito sobre os 20%. <b>Se as notas não chegam aos 40%, a área é tratada como mista.</b></p>'),
  ('Os números', '<p>A mesma casa, nos três enquadramentos. Para a redução de pré-fabricado, as notas do fabricante teriam de somar %s.</p>' % brl(N.NOTAS)
   + fig([N.bar('Alvenaria, sem planejamento', N.INSS_ALV, N.INSS_ALV, 'mute'), N.bar('Tipo misto', N.INSS_MIS, N.INSS_ALV, small='estrutura de metal comprovada por nota'),
          N.bar('Pré-fabricado', N.INSS_PRE, N.INSS_ALV, 'hl', 'notas de 40% do custo da obra')],
         'Contribuição apurada na aferição', CASA,
         'Contribuição apurada: alvenaria sem planejamento, %s; tipo misto, %s; pré-fabricado comprovado, %s.' % (brl(N.INSS_ALV), brl(N.INSS_MIS), brl(N.INSS_PRE)))),
  ('O que não conta', '<ul><li>Notas de laje pré-moldada, fundação, piso, cobertura e paredes internas.</li>'
   '<li>Notas de elétrica, hidráulica e outros serviços complementares.</li>'
   '<li>Painel fabricado pela própria construtora.</li>'
   '<li>Montagem cuja mão de obra já foi declarada e usada como dedução na aferição.</li></ul>'),
  ('Na prática', '<p>A decisão é tomada antes da compra do aço. Painel feito em fábrica, com nota de venda e de montagem: o caminho é o pré-fabricado. Estrutura montada peça a peça no canteiro: o caminho é o tipo misto, com a nota da estrutura guardada.</p>'
   '<p>Há um terceiro caminho, que vale para qualquer sistema construtivo: a mão de obra declarada durante a obra. <a href="b-fator-de-ajuste.html">Quando ela chega à metade da remuneração apurada, a aferição fecha sem saldo.</a></p>'
   '<p style="margin-top:2em"><a class="lnk" href="inss.html#simulador">Simular o INSS da minha obra</a></p>'),
 ],
 fontes=[(F_IN2021[0] + ' Art. 7º, XIV; art. 25, §§ 16 a 19; art. 26, §§ 2º e 3º.', F_IN2021[1]), (F_MANUAL[0] + ' Classificação do tipo da obra e item 19.5.', F_MANUAL[1])],
 rel=['fator-de-ajuste', 'cno-prazo-e-inscricao'], call='Vai construir em steel frame?'),

dict(slug='cno-prazo-e-inscricao', tema='imposto', mins=4,
 title='CNO: quem inscreve a obra e em que prazo',
 h1='CNO: a obra tem 30 dias <b>para existir na Receita.</b>',
 lead='O Cadastro Nacional de Obras é o registro da construção na Receita Federal. <b>É nele que a obra recebe tipo, área e destinação, os três dados que definem o INSS no fim.</b>',
 resumo='Quem é o responsável, o prazo de 30 dias e os três campos que definem o imposto.',
 desc='CNO, o Cadastro Nacional de Obras: quem deve inscrever a obra, o prazo de 30 dias, as obras dispensadas e por que tipo, área e destinação definem o INSS.',
 body=[
  ('Resposta curta', '<p class="big">Toda obra de construção civil é inscrita no CNO em até 30 dias, contados do início. Quem inscreve é o responsável pela obra: o proprietário, o dono da obra ou a construtora contratada por empreitada total.</p>'),
  ('O que é', '<p>O CNO é o banco de dados da Receita Federal com as informações cadastrais das obras e dos seus responsáveis. Construção, demolição, reforma e ampliação entram na definição de obra.</p>'
   '<p>Duas situações ficam dispensadas: a casa que atende às condições de isenção, descritas no fim deste artigo, e a reforma de pequeno valor feita por pessoa jurídica com contabilidade regular.</p>'),
  ('Quem inscreve', '<table class="tb"><thead><tr><th scope="col">Como a obra é executada</th><th scope="col">Quem inscreve</th></tr></thead><tbody>'
   '<tr><th scope="row">Pelo proprietário ou dono da obra</th><td>o proprietário do imóvel ou o dono da obra</td></tr>'
   '<tr><th scope="row">Por construtora, em empreitada total</th><td>a construtora</td></tr>'
   '<tr><th scope="row">Por empreitada parcial, ou por contratada que não é construtora</th><td>quem contratou</td></tr>'
   '</tbody></table>'
   '<p>Quem tem vínculo com o imóvel e precisa da certidão também pode inscrever a obra, mesmo sem ser o responsável.</p>'),
  ('Prazos', '<ol class="steps three">'
   '<li><h3>Inscrição</h3><p>Até 30 dias do início da obra, com todos os responsáveis informados.</p><span class="k">IN RFB 2.061, art. 18</span></li>'
   '<li><h3>Alterações</h3><p>Mudou um dado do cadastro: 30 dias para informar, contados da mudança.</p><span class="k">IN RFB 2.061, art. 19</span></li>'
   '<li><h3>Paralisação</h3><p>Obra parada é informada no CNO. É o que justifica a falta de declaração nos meses sem atividade.</p><span class="k">IN RFB 2.021, art. 33, § 1º, X</span></li>'
   '</ol>'
   '<p style="margin-top:2.4em">Perder o prazo de inscrição sujeita o responsável a multa. Informação omitida, inexata ou incompleta, também.</p>'
   '<p>A inscrição é feita pela internet, no sistema CNO, e não exige documento no ato. A comprovação é pedida depois, se a Receita solicitar.</p>'),
  ('Uma inscrição por projeto', '<p>A inscrição é única por projeto e reúne todas as obras previstas nele. Casa, edícula e piscina do mesmo projeto ficam sob o mesmo número.</p>'),
  ('Por que importa', '<p>O que é informado no CNO alimenta o cálculo da aferição. Três campos pesam.</p>'
   '<ul><li><b>Tipo.</b> Alvenaria, madeira ou mista. Define se a mão de obra presumida é 20% ou 15% do custo.</li>'
   '<li><b>Área.</b> Principal e complementar. Piscina e garagem térrea fora do corpo da casa, quando discriminadas no projeto, entram com redução.</li>'
   '<li><b>Destinação.</b> Residencial unifamiliar, multifamiliar, comercial ou galpão. Cada uma tem o seu valor por m².</li></ul>'
   '<p>Corrigir depois é possível, e parte das alterações pede processo digital com documento. <b>Inscrever certo custa menos do que retificar.</b></p>'),
  ('Isenção', '<p>Não precisa de inscrição nem recolhe contribuição a casa que reúne todas estas condições: proprietário pessoa física, sem outro imóvel; residencial e unifamiliar; até 70 m² de área total; uso próprio; tipo econômico ou popular; executada sem mão de obra remunerada.</p>'
   '<p>No cartório, a certidão é substituída por uma declaração do proprietário, sob as penas da lei.</p>'),
 ],
 fontes=[(F_IN2061[0] + ' Arts. 1º a 6º, 17 a 19, 21 e 22.', F_IN2061[1]), (F_IN2021[0] + ' Art. 7º, XVI; art. 33; art. 34; art. 43.', F_IN2021[1]), F_L8212],
 rel=['steel-frame-paga-menos-inss', 'obra-antiga-decadencia'], call='Vai começar uma obra?'),

dict(slug='obra-antiga-decadencia', tema='imposto', mins=4,
 title='Construí há mais de cinco anos. Ainda devo INSS?',
 h1='Obra antiga: <b>passado o prazo, a Receita não cobra mais.</b>',
 lead='É a decadência. O prazo corre a favor de quem construiu, mas a prova é dele. <b>A regularização continua necessária, e a data precisa de documento.</b>',
 resumo='O prazo de decadência, o cálculo proporcional e os documentos que provam a data.',
 desc='Decadência no INSS de obra: quando a construção com mais de cinco anos não paga contribuição, como é o cálculo proporcional e quais documentos provam início e término.',
 body=[
  ('Resposta curta', '<p class="big">A Receita tem cinco anos para cobrar, contados do primeiro dia do ano seguinte. Passado o prazo, a obra é regularizada sem contribuição a recolher, desde que a data seja provada.</p>'),
  ('O prazo', '<p>O direito de a Receita constituir o crédito extingue-se no prazo de decadência do Código Tributário Nacional: cinco anos, contados do primeiro dia do exercício seguinte àquele em que o lançamento poderia ter sido feito.</p>'
   '<p>Não são cinco anos corridos. O Manual do Sero dá o exemplo: em aferição feita em 2024, está decaído o que ocorreu até 31 de dezembro de 2018.</p>'
   '<p>Na prática, quem faz a conta é o sistema. As datas de início e de término são informadas na aferição, e o Sero reconhece o período atingido.</p>'),
  ('Como funciona', '<p>O caminho é o mesmo de qualquer obra: inscrição no CNO e aferição no Sero. Muda o resultado.</p>'
   '<p>Se toda a obra está em período decaído, não há contribuição a recolher. Se uma parte é antiga e outra é recente, o cálculo é proporcional: a contribuição incide só sobre os meses não atingidos.</p>'
   '<p class="note">Exemplo: obra de 24 meses, com 18 em período decaído. A remuneração apurada é multiplicada por 6/24.</p>'),
  ('A prova do início', '<p>Vale o documento mais antigo, desde que tenha vínculo com a obra e seja da época.</p>'
   '<ul><li>Comprovante de recolhimento de contribuições vinculado à obra.</li><li>Nota fiscal de prestação de serviços.</li><li>Recibo de pagamento a trabalhadores.</li>'
   '<li>Comprovante de ligação ou conta de água ou de energia.</li><li>Nota de compra de material com o endereço da obra como local de entrega.</li>'
   '<li>Alvará de construção.</li><li>Contrato com instituição financeira firmado na época.</li></ul>'),
  ('A prova do término', '<ul><li>Habite-se ou certidão de conclusão de obra.</li><li>Comprovante de IPTU em que conste a área da edificação.</li>'
   '<li>Certidão de lançamento tributário com o histórico do IPTU.</li><li>Auto de regularização ou de conclusão, ou certidão da prefeitura, com número de cadastro, área construída e data.</li>'
   '<li>Escritura de compra e venda em que conste a área construída.</li><li>Contrato de locação com firma reconhecida na época.</li>'
   '<li>Contrato com instituição financeira que descreva o imóvel e a área.</li></ul>'
   '<p>Na falta desses, a Receita aceita um conjunto de pelo menos três documentos, entre eles conta de luz ou de telefone, correspondência bancária para o endereço e declaração de imposto de renda da época com o imóvel descrito.</p>'),
  ('O erro que custa', '<p>Regularizar obra antiga sem reunir os documentos antes. As datas são informadas por quem regulariza, e a Receita pode pedir a comprovação. <b>Data sem documento não se sustenta.</b></p>'
   '<p>Antes de abrir a aferição, separe o IPTU antigo, a certidão da prefeitura e tudo o que ligar a construção à data.</p>'),
 ],
 fontes=[(F_IN2021[0] + ' Arts. 29 e 42.', F_IN2021[1]), F_CTN, (F_MANUAL[0] + ' Item 20, Decadência.', F_MANUAL[1]), F_DECAD],
 rel=['cno-prazo-e-inscricao', 'fator-de-ajuste'], call='Tem uma construção antiga para regularizar?'),

dict(slug='fator-de-ajuste', tema='imposto', mins=4,
 title='Fator de ajuste: quando a aferição fecha em zero',
 h1='Fator de ajuste: <b>quem declarou a mão de obra não paga duas vezes.</b>',
 lead='Para a pessoa física que construiu com mão de obra declarada, a norma tem uma regra de fechamento. <b>Atingido o mínimo, a aferição termina sem contribuição a recolher.</b>',
 resumo='O mínimo de 50% de mão de obra declarada e a entrega em todos os meses.',
 desc='Fator de ajuste no INSS de obra: quando a pessoa física que declarou a mão de obra fecha a aferição sem saldo, o mínimo de 50% ou 70% e o que derruba a regra.',
 body=[
  ('Resposta curta', '<p class="big">Se a remuneração declarada durante a obra chega a 50% da mão de obra apurada pela Receita, e a declaração foi entregue em todos os meses, a aferição é transmitida sem débito. Acima de 350 m², o mínimo é 70%.</p>'),
  ('Quem pode usar', '<p>A regra vale para obra predial de responsabilidade de pessoa física. As duas condições são cumulativas.</p>'
   '<ol><li>Remuneração declarada ou recolhida de pelo menos 50% da remuneração total apurada, nas obras de até 350 m², ou de 70%, acima disso.</li>'
   '<li>DCTFWeb apresentada para todo o período de execução da obra.</li></ol>'),
  ('O que entra na conta', '<ul><li>Mão de obra própria, contratada diretamente pelo responsável e informada ao eSocial, com a DCTFWeb transmitida.</li>'
   '<li>Mão de obra terceirizada, declarada pela empreiteira ou subempreiteira com vínculo à obra.</li>'
   '<li>Remuneração paga a autônomo ou a MEI contratado para a obra, quando declarada.</li></ul>'
   '<p>Tudo precisa ter vínculo com a inscrição da obra no CNO e estar dentro do período da aferição.</p>'),
  ('Os números', '<p>Na casa de %d m² do nosso exemplo, a Receita apura %s de remuneração. Metade disso é %s.</p>' % (N.AREA, brl(N.RMT_ALV), brl(N.RMT_ALV * .5))
   + fig([N.bar('Remuneração apurada', N.RMT_ALV, N.RMT_ALV, 'mute'), N.bar('Mínimo declarado', N.RMT_ALV * .5, N.RMT_ALV, 'hl', '50%, obra de até 350 m²')],
         'O mínimo para a aferição fechar sem saldo', CASA + ' · tipo alvenaria',
         'Remuneração apurada, %s; mínimo declarado, %s.' % (brl(N.RMT_ALV), brl(N.RMT_ALV * .5)))
   + '<p>Se a obra declarou pelo menos esse valor ao longo dos meses, a aferição fecha sem saldo. As contribuições já foram pagas mês a mês, sobre a remuneração real.</p>'),
  ('Onde a regra falha', '<ul><li><b>Um mês sem declaração.</b> A entrega precisa ser ininterrupta. Obra parada é informada no CNO: a paralisação justifica os meses sem DCTFWeb.</li>'
   '<li><b>Remuneração sem vínculo com a obra.</b> O que não está ligado à inscrição no CNO não é aproveitado.</li>'
   '<li><b>Declaração abaixo do mínimo.</b> O que foi declarado abate a base, mas a diferença é cobrada.</li></ul>'),
  ('E o steel frame', '<p>O fator de ajuste não depende do sistema construtivo. No steel frame, soma-se a ele a escolha do tipo da obra. <a href="b-steel-frame-paga-menos-inss.html">Com o tipo misto, a remuneração apurada é menor</a> e, com ela, o mínimo a declarar.</p>'
   '<p style="margin-top:2em"><a class="lnk" href="inss.html#simulador">Simular o INSS da minha obra</a></p>'),
 ],
 fontes=[(F_IN2021[0] + ' Arts. 24 e 31 a 33.', F_IN2021[1]), (F_MANUAL[0] + ' Item 22, Fator de Ajuste.', F_MANUAL[1])],
 rel=['steel-frame-paga-menos-inss', 'cno-prazo-e-inscricao'], call='Quer a obra declarada do jeito certo?'),

dict(slug='steel-frame-e-mais-caro', tema='steel frame', mins=4,
 title='Steel frame é mais caro?',
 h1='Steel frame é mais caro? <b>Na planilha de materiais, quase sempre. Na conta inteira, depende.</b>',
 lead='Quem compara só o custo direto costuma parar na alvenaria. <b>Prazo, repetição e imposto mudam o resultado, e o imposto é a parte que quase ninguém põe na conta.</b>',
 resumo='O que os comparativos mostram, o que eles deixam de fora e onde o INSS entra.',
 desc='Steel frame é mais caro que alvenaria? O que os comparativos acadêmicos mostram, o que fica fora da planilha e como o INSS de obra entra na conta.',
 body=[
  ('Resposta curta', '<p class="big">No custo direto, a maioria dos comparativos brasileiros encontra o steel frame acima da alvenaria. A diferença cai, e às vezes se inverte, quando entram o prazo de obra, a repetição do projeto e o INSS.</p>'),
  ('O que os estudos mostram', '<p>Os comparativos publicados por universidades brasileiras são estudos de caso: uma casa, uma cidade, uma data. Não chegam ao mesmo número, nem ao mesmo sinal.</p>'
   '<ul><li>A maior parte encontra custo direto maior no steel frame, com a estrutura como o item que mais pesa.</li>'
   '<li>Alguns encontram o contrário, em geral quando há repetição de unidades ou quando o prazo entra na conta.</li>'
   '<li>Quase todos registram obra mais curta.</li></ul>'
   '<p>A conclusão honesta é que não existe um percentual que valha para toda obra. Existe a conta de cada projeto.</p>'),
  ('O que fica fora da planilha', '<ul><li><b>Prazo.</b> Obra mais curta custa menos em canteiro, administração e aluguel pago enquanto a casa não fica pronta.</li>'
   '<li><b>Projeto.</b> No steel frame o aço é comprado e cortado pelo projeto. O que não foi resolvido no desenho vira retrabalho caro, e o que foi resolvido vira previsibilidade.</li>'
   '<li><b>Fornecedor.</b> A distância da fábrica e o frete pesam. Mão de obra de montagem treinada também.</li>'
   '<li><b>Repetição.</b> Painel que se repete dilui o custo de engenharia e de fabricação.</li></ul>'),
  ('O imposto na conta', '<p>É a linha que falta em quase todo comparativo. A casa em steel frame pode ser enquadrada como obra do tipo misto ou como pré-fabricado, e isso muda o INSS apurado no fim.</p>'
   + fig([N.bar('Alvenaria, sem planejamento', N.INSS_ALV, N.INSS_ALV, 'mute'), N.bar('Steel frame, tipo misto', N.INSS_MIS, N.INSS_ALV, small='estrutura de metal comprovada por nota'),
          N.bar('Steel frame, pré-fabricado', N.INSS_PRE, N.INSS_ALV, 'hl', 'notas de 40% do custo da obra')],
         'INSS apurado na aferição', CASA,
         'INSS apurado: alvenaria sem planejamento, %s; steel frame como tipo misto, %s; steel frame com pré-fabricado comprovado, %s.' % (brl(N.INSS_ALV), brl(N.INSS_MIS), brl(N.INSS_PRE)))
   + '<p><a href="b-steel-frame-paga-menos-inss.html">Como cada enquadramento funciona e que notas ele exige.</a></p>'),
  ('Como comparar orçamentos', '<ol><li>Compare a casa pronta, com o mesmo acabamento, e não o metro quadrado de parede.</li>'
   '<li>Ponha o prazo em reais: meses de canteiro, de aluguel e de juros.</li>'
   '<li>Peça o orçamento do steel frame com projeto executivo, para a quantidade de aço não ser estimativa.</li>'
   '<li>Inclua o INSS da obra nos dois cenários, com o enquadramento que cada um permite.</li></ol>'
   '<p style="margin-top:2em"><a class="lnk" href="inss.html#simulador">Simular o INSS da minha obra</a></p>'),
 ],
 fontes=[('Comparativo de custo entre light steel frame e alvenaria convencional, estudo de caso em Goiânia. PUC Goiás.', 'https://repositorio.pucgoias.edu.br/jspui/bitstream/123456789/877/1/TCC2_042_vers%c3%a3o%20final.pdf'),
         ('Análise comparativa orçamentária dos sistemas construtivos convencional e light steel frame. Unipar.', 'https://www.unipar.br/documentos/259/ANALISE_COMPARATIVA_ORCAMENTARIA_DOS_SISTEMAS_CONSTRUTIVOS_CONVENCIONAL.pdf'),
         ('Estudo de caso comparativo em Palmas, TO. Ceulp/Ulbra, 2017.', 'https://ulbra-to.br/bibliotecadigital/uploads/document5f3e6bff22ac8.pdf'),
         (F_IN2021[0] + ' Arts. 25 e 26.', F_IN2021[1])],
 rel=['steel-frame-paga-menos-inss', 'steel-frame-conforto-termoacustico'], call='Quer a conta inteira do seu projeto?'),

dict(slug='steel-frame-conforto-termoacustico', tema='steel frame', mins=4,
 title='Steel frame tem melhor conforto termoacústico?',
 h1='Conforto térmico e acústico: <b>quem responde é a parede, não o aço.</b>',
 lead='A parede de steel frame é um conjunto de camadas. <b>Com lã mineral no miolo, o isolamento de som medido em laboratório passa com folga do mínimo. No calor, o resultado depende do projeto.</b>',
 resumo='O que o ensaio do IPT mediu em som e o que a simulação mostrou em temperatura.',
 desc='Conforto térmico e acústico do steel frame: resultados de ensaio de isolamento sonoro e de simulação térmica em documento de avaliação técnica do IPT, e o que o projeto precisa garantir.',
 body=[
  ('Resposta curta', '<p class="big">No som, sim: a parede com lã de vidro no miolo isolou bem acima do mínimo exigido. No calor, depende: isolante, cor da fachada, sombreamento e ventilação decidem se a casa atende ou não.</p>'),
  ('A parede', '<p>No sistema avaliado pelo IPT, a parede externa tem quatro camadas: placa cimentícia por fora, perfis de aço zincado, manta de lã de vidro de 50 mm no miolo e chapa de gesso para drywall por dentro.</p>'
   '<p>O aço sustenta. Quem isola é o conjunto: duas placas separadas por uma câmara preenchida com lã.</p>'),
  ('Som', '<p>O ensaio de laboratório mediu o índice de redução sonora da parede de fachada e da parede entre duas casas geminadas.</p>'
   '<table class="tb"><thead><tr><th scope="col">Parede</th><th scope="col">Mínimo exigido</th><th scope="col">Medido em laboratório</th></tr></thead><tbody>'
   '<tr><th scope="row">Fachada</th><td>30 dB</td><td class="hl">50 dB</td></tr>'
   '<tr><th scope="row">Entre unidades</th><td>45 dB</td><td class="hl">51 dB</td></tr></tbody></table>'
   '<p>O número vale para a parede. Na casa pronta, a janela costuma ser o ponto fraco: a fachada só entrega o que a esquadria permite.</p>'),
  ('Calor', '<p>O desempenho térmico foi avaliado por simulação nas oito zonas bioclimáticas do país. O sistema atendeu ao critério mínimo, com condições.</p>'
   '<ul><li>Lã de vidro de 50 mm nas paredes, em todo o perímetro, e sobre o forro. Na zona 8, 100 mm sobre o forro.</li>'
   '<li>Beiral de 60 cm.</li>'
   '<li>Fachada em cor clara ou média, conforme a zona.</li>'
   '<li>Em parte das zonas, só com janelas sombreadas, com ventilação, ou com as duas coisas.</li></ul>'
   '<p>A parede leve tem pouca massa para acumular calor. O conforto vem do isolamento e do projeto: orientação, sombra e ventilação cruzada.</p>'),
  ('O que isso quer dizer', '<p>Steel frame não é mais confortável nem menos confortável por ser steel frame. Com as camadas certas, isola o som melhor do que a norma pede. Sem isolante, ou com fachada escura sem sombra, perde.</p>'
   '<p><b>Conforto se especifica no projeto:</b> espessura da lã, tipo de placa, cor, beiral e esquadria.</p>'
   '<p class="note">Os números são do Documento de Avaliação Técnica nº 14 do SINAT, emitido em 2013 com avaliação do IPT, para um sistema específico de casas térreas. Valem como referência de ordem de grandeza. Cada projeto tem a sua composição de parede.</p>'),
 ],
 fontes=[('SINAT. Documento de Avaliação Técnica nº 14, Sistema construtivo a seco em light steel frame. Avaliação técnica do IPT, abril de 2013.', 'https://www.cbca-acobrasil.org.br/upfiles/downloads/Datec-14-LSF.pdf')],
 rel=['steel-frame-e-mais-caro', 'steel-frame-paga-menos-inss'], call='Vai construir em steel frame?'),
]
