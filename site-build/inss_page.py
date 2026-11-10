# -*- coding: utf-8 -*-
# Página de INSS de obra do site L. Engenharia.
# Fonte única dos números do exemplo: os mesmos valores vão para a home e para o vídeo.
# Regras conferidas no texto consolidado da IN RFB 2.021/2021, na IN RFB 2.061/2021 e no Manual do Sero v3.0 (08/2024).
import json, re, html

AREA = 150          # m², casa do exemplo
VAU = 2000          # R$/m², valor de referência (o oficial é consultado no Sero, por mês, UF e destinação)
EQ = .89            # área equivalente, residencial unifamiliar até 1.000 m² (IN 2.021, art. 25, § 6º, I, a)
P_ALV = .20         # mão de obra presumida, tipo alvenaria (art. 25, § 16, I)
P_MISTA = .15       # tipo madeira ou mista (art. 25, § 16, II)
FS = .40            # fator social, de 100 a 200 m² (art. 26, § 1º, II)
RED_PRE = .70       # redução por pré-fabricado (art. 26, § 2º)
MIN_NOTAS = .40     # notas do fabricante sobre o custo da obra (art. 26, § 2º, II)
ALIQ = .368         # soma das alíquotas (Manual do Sero, item 23)

def brl(v): return 'R$ ' + format(int(round(v)), ',d').replace(',', '.')
def dec(v, n=1): return format(v, ',.%df' % n).replace(',', 'X').replace('.', ',').replace('X', '.')

AEQ = AREA * EQ
COD = AEQ * VAU
MO_ALV = COD * P_ALV; MO_MIS = COD * P_MISTA
RMT_ALV = MO_ALV * FS; RMT_MIS = MO_MIS * FS
INSS_ALV = RMT_ALV * ALIQ; INSS_MIS = RMT_MIS * ALIQ
RMT_PRE = RMT_ALV * (1 - RED_PRE); INSS_PRE = RMT_PRE * ALIQ
ECON = round(INSS_ALV) - round(INSS_PRE)
NOTAS = COD * MIN_NOTAS

# números que a home e o vídeo repetem
NUM = dict(area='%d m²' % AREA, sem=brl(INSS_ALV), com=brl(INSS_PRE), econ=brl(ECON), mista=brl(INSS_MIS))

def pct(v, base): return ('%.2f' % (100 * v / base)).rstrip('0').rstrip('.')

URL_IN2021 = 'http://normas.receita.fazenda.gov.br/sijut2consulta/link.action?visao=anotado&idAto=116968'
URL_IN2061 = 'http://normas.receita.fazenda.gov.br/sijut2consulta/link.action?visao=anotado&idAto=122299'
URL_MANUAL = 'https://www.gov.br/receitafederal/pt-br/assuntos/construcao-civil/sero/manual-do-sero'
URL_SERO = 'https://www.gov.br/receitafederal/pt-br/assuntos/construcao-civil/sero'
URL_LEI8212 = 'https://www.planalto.gov.br/ccivil_03/leis/l8212cons.htm'
URL_CTN = 'https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm'

# perguntas frequentes: (pergunta, resposta em html)
FAQ = [
 ('Toda obra paga INSS?',
  '<p>Paga quando há mão de obra remunerada. A exceção é a casa própria de até 70 m², residencial e unifamiliar, de tipo econômico ou popular, erguida sem mão de obra remunerada por pessoa física que não tenha outro imóvel. As condições valem juntas.</p>'),
 ('Quem responde pelo INSS da obra: eu ou a construtora?',
  '<p>O proprietário do imóvel ou o dono da obra. Quando uma construtora é contratada por empreitada total, a responsabilidade pela obra é dela, e ela responde solidariamente com o proprietário. Em contrato por administração, a responsabilidade continua com quem contratou.</p>'),
 ('O que é o CNO e qual é o prazo?',
  '<p>É o Cadastro Nacional de Obras, da Receita Federal. A inscrição deve ser feita em até 30 dias, contados do início da obra, com todos os responsáveis informados. Perder o prazo sujeita o responsável a multa.</p>'),
 ('O que é a aferição e quando ela é feita?',
  '<p>É o fechamento da conta no Sero, o serviço eletrônico da Receita, quando a obra termina. O sistema calcula a remuneração da mão de obra, abate o que foi declarado e recolhido durante a obra e gera a DCTFWeb Aferição de Obras. O DARF vence no dia 20 do mês seguinte ao envio.</p>'),
 ('E se eu não regularizar a obra?',
  '<p>A Receita Federal monitora as obras com base nos alvarás e habite-se emitidos pelas prefeituras e envia aviso ao responsável. Quem não regulariza no prazo do aviso pode ser fiscalizado e ter as contribuições lançadas com multa de 75% a 225% do valor devido.</p><p>Pela lei federal, a averbação da construção no registro de imóveis pede a certidão negativa da obra. Há estados em que a corregedoria dos cartórios dispensou a exigência. A contribuição continua devida do mesmo jeito.</p>'),
 ('Steel frame paga menos INSS que alvenaria?',
  '<p>Pode pagar. Com a estrutura de metal comprovada por nota fiscal, a obra é do tipo mista e a mão de obra presumida cai de 20% para 15% do custo. Com estrutura e paredes externas feitas em fábrica e notas que somem 40% do custo apurado, a remuneração cai 70%.</p><p>Sem nota e sem enquadramento, a casa em steel frame é calculada como alvenaria.</p>'),
 ('Que notas fiscais contam para a redução de pré-fabricado?',
  '<p>As de venda da estrutura e das paredes externas pré-fabricadas e as de instalação ou montagem, emitidas pelo fabricante ou por quem montou.</p><p>Não contam notas de laje, fundação, piso, cobertura e paredes internas, nem as de elétrica, hidráulica e outros serviços complementares.</p>'),
 ('Contratei pedreiro sem registro. E agora?',
  '<p>Sem remuneração declarada não há o que abater: a contribuição incide sobre toda a mão de obra presumida pela área. Continuam valendo o fator social, o enquadramento correto do tipo de obra e, se for o caso, a decadência.</p>'),
 ('Paguei autônomo ou MEI. Isso abate?',
  '<p>Abate quando a remuneração foi declarada e tem vínculo com a obra. As contribuições recolhidas sobre o que foi pago a autônomo ou a MEI contratado para a obra são aproveitadas para deduzir a contribuição patronal apurada na aferição.</p>'),
 ('Construí há mais de cinco anos. Ainda devo?',
  '<p>A Receita tem cinco anos para lançar a contribuição, contados do primeiro dia do ano seguinte. Em aferição feita em 2024, por exemplo, estava decaído o que ocorreu até 31 de dezembro de 2018. Cabe ao responsável provar quando a obra terminou: habite-se, IPTU com a área construída, certidão da prefeitura, escritura ou contrato de financiamento da época.</p><p>Se só uma parte da obra é antiga, a contribuição incide apenas sobre o período recente.</p>'),
 ('Reforma e ampliação pagam?',
  '<p>Pagam, com regra própria. Na reforma, a remuneração devida tem redução de 65%. Na ampliação, a conta é feita só sobre a área acrescida. Na demolição, a redução é de 90%.</p>'),
 ('Piscina e garagem entram na área?',
  '<p>Entram com peso menor. Piscina, quadra esportiva e garagem térrea fora da projeção da casa são áreas complementares: redução de 50% quando cobertas e de 75% quando descobertas. Precisam estar discriminadas no projeto. Sem isso, são calculadas como área principal.</p>'),
 ('O valor do simulador é o que eu vou pagar?',
  '<p>É uma estimativa. O cálculo oficial usa o VAU do mês da aferição, por estado e por destinação da obra, consultado no próprio Sero. O simulador usa R$ %s por m² como referência e considera casa unifamiliar de pessoa física, obra nova.</p>' % format(VAU, ',d').replace(',', '.')),
 ('E o ISS da obra?',
  '<p>É outro imposto. O ISS é municipal, cobrado pela prefeitura, e cada cidade tem a sua regra. O INSS da obra é federal e segue a mesma norma no país inteiro.</p>'),
 ('Quando contratar a engenharia tributária?',
  '<p>Antes de comprar o aço. O enquadramento depende de como a obra é inscrita no CNO e de como as notas são emitidas. Com a obra pronta, resta conferir o cálculo e aproveitar o que já está documentado.</p>'),
]

def _plain(h): return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h))).strip()
FAQ_LD = '<script type="application/ld+json">' + json.dumps({
    '@context': 'https://schema.org', '@type': 'FAQPage',
    'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': _plain(a)}} for q, a in FAQ]},
    ensure_ascii=False).replace('</', '<\\/') + '</script>'

def bar(label, value, base, cls='', small=''):
    return ('<div class="r%s"><span class="l">%s%s</span><span class="t"><i style="width:%s%%"></i></span><span class="v">%s</span></div>'
            % (' ' + cls if cls else '', label, '<small>%s</small>' % small if small else '', pct(value, base), brl(value)))

_BODY = '''<main>
<section class="col phead"><p class="crumb">engenharia tributária</p>
<h1>A obra paga INSS. <b>Quase sempre a mais.</b></h1>
<p class="lead" style="margin-top:26px">Toda obra recolhe contribuição previdenciária sobre a mão de obra. Quando o dono não comprova o que pagou, a Receita Federal presume pela área construída. <b>A norma prevê três caminhos para pagar só o devido, e o steel frame pode usar todos.</b></p></section>

<section class="band sec-s" id="imposto"><div class="tag"><b>O imposto</b></div><div class="prose">
<h2>O que é o INSS da obra</h2>
<p>Pedreiro, montador, eletricista: sobre a remuneração de quem trabalha na obra incidem a contribuição previdenciária e as contribuições de terceiros. Quem responde é o proprietário do imóvel ou o dono da obra. Na empreitada total, a construtora.</p>
<p>A conta fecha no fim, na aferição. A lei federal pede a certidão negativa da obra para averbar a construção na matrícula do imóvel, e quem financia pela Caixa só recebe a última parcela com a averbação feita.</p>
<p>A Receita acompanha as obras pelos alvarás e habite-se que as prefeituras informam. <b>Quem recebe o aviso e não regulariza pode ser fiscalizado, com multa de 75% a 225% sobre o valor devido.</b></p>
<div class="nums" style="margin-top:48px">
<div><div class="num">36,8%</div><div class="nl">soma das alíquotas sobre a mão de obra apurada</div></div>
<div><div class="num">30 dias</div><div class="nl">do início da obra para a inscrição no CNO, o Cadastro Nacional de Obras</div></div>
<div><div class="num">dia 20</div><div class="nl">do mês seguinte à aferição: vencimento do DARF</div></div>
</div>
</div></section>

<section class="band sec" id="calculo"><div class="tag"><b>O cálculo</b></div><div class="prose">
<h2>Sem comprovação, vale a área construída</h2>
<p>É a aferição indireta. O Sero, serviço eletrônico da Receita Federal, parte da área do projeto e chega à contribuição em quatro passos.</p>
<ol class="steps" style="margin-top:48px">
<li><h3>Custo da obra</h3><p>Área equivalente vezes o VAU. Na casa unifamiliar, a área equivalente é 89% da área principal. O VAU é o valor por m² que a Receita atualiza todo mês, por estado e por destinação.</p><span class="k">[[AREA]] m² × 89% × [[VAU]] = [[COD]]</span></li>
<li><h3>Mão de obra presumida</h3><p>Um percentual do custo, conforme o tipo da obra: 20% na alvenaria, 15% na madeira ou mista.</p><span class="k">20% = [[MO_ALV]]</span></li>
<li><h3>Fator social</h3><p>Só para pessoa física. Reduz a base conforme a área total: quanto menor a obra, maior a redução.</p><span class="k">de 100 a 200 m², 40% = [[RMT_ALV]]</span></li>
<li><h3>Alíquota</h3><p>36,8% sobre a remuneração apurada, depois de abatido o que foi declarado e recolhido durante a obra.</p><span class="k">36,8% = [[INSS_ALV]]</span></li>
</ol>
<figure class="fig" style="margin-top:72px"><div class="bars" role="img" aria-label="Do custo presumido à contribuição: custo da obra [[COD]]; mão de obra presumida [[MO_ALV]]; depois do fator social [[RMT_ALV]]; contribuição [[INSS_ALV]].">
[[BARS1]]
</div><figcaption class="cap"><b>Do custo presumido à contribuição</b><span>casa de [[AREA]] m² · pessoa física · tipo alvenaria</span></figcaption></figure>
<h3>Fator social, por área total da obra</h3>
<table class="tb"><thead><tr><th scope="col">Área total</th><th scope="col">Percentual aplicado à base</th></tr></thead><tbody>
<tr><th scope="row">Até 100 m²</th><td>20%</td></tr>
<tr><th scope="row">De 100 a 200 m²</th><td>40%</td></tr>
<tr><th scope="row">De 200 a 300 m²</th><td>55%</td></tr>
<tr><th scope="row">De 300 a 400 m²</th><td>70%</td></tr>
<tr><th scope="row">Acima de 400 m²</th><td>90%</td></tr>
</tbody></table>
</div></section>

<section class="band sec" id="economizar"><div class="tag"><b>Como economizar</b></div><div class="prose">
<h2>Três caminhos previstos na norma</h2>
<div class="sys" style="margin-top:40px">
<div><h3>Enquadrar o tipo da obra</h3><p>Estrutura ou paredes externas de metal, de madeira ou pré-fabricadas: a obra é do tipo mista. <b>A mão de obra presumida cai de 20% para 15% do custo.</b> A prova é a nota fiscal da estrutura.</p><span class="k">base 25% menor</span></div>
<div><h3>Comprovar o pré-fabricado</h3><p>Estrutura e paredes externas feitas em fábrica e montadas na obra: <b>a remuneração apurada cai 70%</b> quando as notas de venda e de montagem somam 40% do custo calculado pela Receita.</p><span class="k">base 70% menor</span></div>
<div><h3>Declarar a mão de obra</h3><p>Para pessoa física: se a remuneração declarada durante a obra chega a 50% da mão de obra apurada, com declaração entregue em todos os meses, <b>não há saldo a pagar na aferição.</b> Acima de 350 m², o mínimo é 70%.</p><span class="k">saldo zero na aferição</span></div>
</div>
<figure class="fig" style="margin-top:72px"><div class="bars" role="img" aria-label="A mesma casa em três enquadramentos: alvenaria sem planejamento, [[INSS_ALV]]; tipo mista, [[INSS_MIS]]; pré-fabricado comprovado, [[INSS_PRE]].">
[[BARS2]]
</div><figcaption class="cap"><b>A mesma casa, três enquadramentos</b><span>[[AREA]] m² · pessoa física · VAU de referência de [[VAU]] por m²</span></figcaption></figure>
<p class="note">As reduções por fator social, pré-fabricado, categoria e destinação da obra são cumulativas. Reforma tem redução de 65% e demolição, de 90%. Piscina, quadra e garagem térrea fora do corpo da casa contam como área complementar, com redução de 50% quando cobertas e de 75% quando descobertas. Concreto e argamassa usinados têm abatimento próprio, calculado sobre o custo da obra.</p>
</div></section>

<section class="band sec" id="steel-frame"><div class="tag"><b>Steel frame</b></div><div class="prose">
<h2>A norma não cita steel frame. <b>Descreve o que ele é.</b></h2>
<p>Nem a instrução normativa nem o Manual do Sero usam a expressão. Trazem dois critérios, e a casa em steel frame pode atender aos dois.</p>
<h3>Estrutura de metal</h3>
<p>A obra é do tipo mista quando “as paredes externas ou a estrutura da edificação forem de madeira, metal ou de material pré-fabricado ou pré-moldado”. No steel frame, a estrutura são os perfis de aço galvanizado. Para sustentar o enquadramento, a Receita pode pedir o projeto aprovado e a nota fiscal da estrutura.</p>
<h3>Componente pré-fabricado</h3>
<p>Para a Receita, pré-fabricado é “o componente ou a parte de uma edificação adquiridos prontos em estabelecimento comercial ou fabricados por antecipação em estabelecimento industrial de terceiros, para posterior instalação ou montagem na obra”. Painel de parede produzido em fábrica e montado no canteiro cabe na definição.</p>
<h3>O que derruba a redução</h3>
<ul>
<li>Notas que somam menos de 40% do custo apurado. A área passa a ser tratada como mista.</li>
<li>Painel fabricado pela própria construtora. Não conta para a redução.</li>
<li>Nota de laje, fundação, piso, cobertura ou parede interna. Não entra na soma. Elétrica e hidráulica também não.</li>
<li>Montagem cuja mão de obra já foi declarada e usada como dedução. A mesma remuneração não conta duas vezes.</li>
</ul>
<p>Os dois critérios não se somam. Para usar a redução de pré-fabricado, a obra é inscrita como alvenaria e o cálculo parte dos 20%. <b>Por isso a escolha é feita antes da compra do aço, não com a obra pronta.</b></p>
</div></section>
<img class="wide obra" src="[[IMG]]" width="[[IMGW]]" height="[[IMGH]]" alt="Modelo da estrutura em light steel frame da Casa Taquaraçu visto por dentro: montantes, guias e treliças de aço galvanizado" loading="lazy" decoding="async" style="object-position:50% 50%">
<div class="col"><div class="cap"><b><a href="o-casa-taquaracu.html">Casa Taquaraçu</a></b><span>montantes, guias e treliças em aço galvanizado</span></div></div>

<section class="band sec" id="passo-a-passo"><div class="tag"><b>Como conseguir</b></div><div class="prose">
<h2>O enquadramento começa antes da obra</h2>
<ol class="steps" style="margin-top:48px">
<li><h3>Antes de começar</h3><p>Inscrição no CNO em até 30 dias do início, com área, destinação e tipo corretos. É aqui que se escolhe o caminho: mista, pré-fabricado ou mão de obra declarada.</p><span class="k">IN RFB 2.061, art. 18</span></li>
<li><h3>Na compra</h3><p>O fabricante emite a nota de venda dos painéis e a de montagem, ou uma só, de venda com montagem. Estrutura e paredes externas ficam separadas do resto.</p><span class="k">IN RFB 2.021, art. 26, § 2º</span></li>
<li><h3>Durante a obra</h3><p>Mão de obra declarada mês a mês, com vínculo à inscrição da obra. Notas e comprovantes guardados: o que não tem vínculo com a obra não abate.</p><span class="k">IN RFB 2.021, arts. 31 a 33</span></li>
<li><h3>Ao terminar</h3><p>Aferição no Sero, DCTFWeb Aferição de Obras, DARF e certidão emitida pela internet. Com a certidão, a averbação no cartório.</p><span class="k">IN RFB 2.021, arts. 6º, 43 e 44</span></li>
</ol>
</div></section>

<section class="band sec" id="exemplo"><div class="tag"><b>Exemplo de obra</b></div><div>
<h2>Casa de [[AREA]] m² em steel frame</h2>
<div class="nums" style="margin-top:34px">
<div><div class="num off">[[INSS_ALV]]</div><div class="nl">aferição indireta, sem planejamento</div></div>
<div><div class="num">[[INSS_PRE]]</div><div class="nl">com pré-fabricado comprovado por nota</div></div>
<div><div class="num sv">[[ECON]]</div><div class="nl">de volta ao orçamento da obra</div></div>
</div>
<h3 style="margin-top:64px">Memória de cálculo</h3>
<dl class="memo" style="margin-top:16px">
<div><dt>Área equivalente</dt><span class="f">[[AREA]] m² × 89%</span><dd>[[AEQ]] m²</dd></div>
<div><dt>Custo da obra por aferição</dt><span class="f">[[AEQ]] m² × [[VAU]]</span><dd>[[COD]]</dd></div>
<div><dt>Mão de obra presumida, obra do tipo alvenaria</dt><span class="f">20%</span><dd>[[MO_ALV]]</dd></div>
<div><dt>Fator social, de 100 a 200 m²</dt><span class="f">40%</span><dd>[[RMT_ALV]]</dd></div>
<div class="res"><dt>Contribuição sem planejamento</dt><span class="f">36,8%</span><dd>[[INSS_ALV]]</dd></div>
<div><dt>Remuneração depois da redução por pré-fabricado</dt><span class="f">− 70%</span><dd>[[RMT_PRE]]</dd></div>
<div class="res"><dt>Contribuição com pré-fabricado comprovado</dt><span class="f">36,8%</span><dd>[[INSS_PRE]]</dd></div>
<div><dt>Notas do fabricante necessárias</dt><span class="f">40% do custo</span><dd>[[NOTAS]]</dd></div>
</dl>
</div></section>

<section class="band sec" id="simulador"><div class="tag"><b>Simulador</b></div><div>
<h2>Quanto a Receita cobraria da sua obra?</h2>
<form id="f" novalidate style="margin-top:34px">
<div class="calc">
<div><label for="area">Área construída (m²)</label><input id="area" type="number" inputmode="decimal" min="1" step="1" placeholder="[[AREA]]" aria-describedby="area-h"><p class="hint" id="area-h" role="alert"></p></div>
<div><label for="sis">Sistema construtivo</label><select id="sis">
<option value="alv">Alvenaria</option><option value="sf">Steel frame</option><option value="wf">Wood frame</option><option value="mod">Modular ou pré-fabricado</option></select></div>
<div><label for="cid">Cidade</label><input id="cid" type="text" placeholder="Marília, SP" autocomplete="address-level2"></div>
</div>
<button class="btn" type="submit">Gerar simulação</button>
</form>
<div class="out" id="out" hidden aria-live="polite">
<p class="meta">Aferição indireta estimada</p>
<div class="num" id="val"></div>
<p>É o que a Receita cobra quando a obra não tem planejamento tributário. <b>Com o enquadramento certo e as notas em ordem, esse valor cai.</b></p>
<p style="margin-top:30px"><a class="lnk" id="wa" href="https://wa.me/5514991850799" target="_blank" rel="noopener">Simular a redução com o especialista</a></p>
</div>
</div></section>

<section class="band sec" id="perguntas"><div class="tag"><b>Perguntas frequentes</b></div><div>
<h2>O que mais perguntam sobre o INSS da obra</h2>
<div class="faq" style="margin-top:34px">
[[FAQ]]
</div>
</div></section>

<section class="band sec"><div class="tag"><b>Fontes</b></div><div>
<ol class="fontes">
<li><span>Instrução Normativa RFB nº 2.021, de 16 de abril de 2021, texto consolidado. Contribuições sobre a mão de obra de obra de construção civil, Sero, aferição e certidão. <a href="[[URL_IN2021]]" target="_blank" rel="noopener">normas.receita.fazenda.gov.br</a></span></li>
<li><span>Instrução Normativa RFB nº 2.061, de 20 de dezembro de 2021. Cadastro Nacional de Obras (CNO). <a href="[[URL_IN2061]]" target="_blank" rel="noopener">normas.receita.fazenda.gov.br</a></span></li>
<li><span>Receita Federal. Manual do Sero, versão 3.0, agosto de 2024. <a href="[[URL_MANUAL]]" target="_blank" rel="noopener">gov.br/receitafederal</a></span></li>
<li><span>Lei nº 8.212, de 24 de julho de 1991, arts. 33, 47 e 49. <a href="[[URL_LEI8212]]" target="_blank" rel="noopener">planalto.gov.br</a></span></li>
<li><span>Código Tributário Nacional, Lei nº 5.172, de 1966, art. 173. <a href="[[URL_CTN]]" target="_blank" rel="noopener">planalto.gov.br</a></span></li>
<li><span>Receita Federal. Recebi um aviso ou intimação. <a href="https://www.gov.br/receitafederal/pt-br/assuntos/construcao-civil/cobranca" target="_blank" rel="noopener">gov.br/receitafederal</a></span></li>
<li><span>Caixa. Cartilha de construção, conclusão, reforma e ampliação de unidades habitacionais isoladas, versão 12, dezembro de 2025. <a href="https://www.caixa.gov.br/Downloads/habitacao-documentos-gerais/cartilha-habitacao-PF-construcao-conclusao-reforma-ampliacao-de-unidades-habitacionais.pdf" target="_blank" rel="noopener">caixa.gov.br</a></span></li>
</ol>
<p class="src" style="margin-top:28px">Conteúdo informativo, conferido nas normas acima em novembro de 2026. Os valores são estimativas para pessoa física, obra nova residencial unifamiliar, sem decadência, com VAU de referência de [[VAU]] por m². O VAU oficial é consultado no Sero. O enquadramento de cada obra é confirmado caso a caso, com o projeto e as notas em mãos.</p>
</div></section>
</main>
<script>(function(){var VAU=[[VAUN]],ALIQ=0.368,PCT={alv:.20,sf:.15,wf:.15,mod:.15},NOME={alv:'Alvenaria',sf:'Steel frame',wf:'Wood frame',mod:'Modular ou pré-fabricado'};
function fs(a){return a<=100?.20:a<=200?.40:a<=300?.55:a<=400?.70:.90}
function eq(a){return a<=1000?.89:.85}
var f=document.getElementById('f'),ar=document.getElementById('area'),h=document.getElementById('area-h'),out=document.getElementById('out');
function brl(v){return 'R$ '+Math.round(v).toLocaleString('pt-BR')}
ar.addEventListener('input',function(){ar.classList.remove('err');h.textContent=''});
f.addEventListener('submit',function(ev){ev.preventDefault();var a=parseFloat(String(ar.value).replace(',','.'));
if(!(a>0)){ar.classList.add('err');h.textContent='Informe a área construída em m².';ar.focus();out.hidden=true;return}
var s=document.getElementById('sis').value,c=document.getElementById('cid').value.trim(),v=a*eq(a)*VAU*PCT[s]*fs(a)*ALIQ;
document.getElementById('val').textContent=brl(v);
var m=['Olá Gustavo, fiz a simulação de INSS no site.','','Área: '+a.toLocaleString('pt-BR')+' m²','Sistema: '+NOME[s]];if(c)m.push('Cidade: '+c);
m.push('Aferição indireta estimada: '+brl(v),'','Quero simular a redução com o especialista.');
document.getElementById('wa').href='https://wa.me/5514991850799?text='+encodeURIComponent(m.join('\\n'));
out.hidden=false;out.scrollIntoView({behavior:'smooth',block:'nearest'})});})();</script>'''

def inss_body(img=('img/inss/estrutura.jpg', 2000, 1125)):
    rep = {
        'AREA': str(AREA), 'VAU': brl(VAU), 'VAUN': str(VAU), 'AEQ': dec(AEQ), 'COD': brl(COD), 'MO_ALV': brl(MO_ALV), 'RMT_ALV': brl(RMT_ALV),
        'INSS_ALV': brl(INSS_ALV), 'INSS_MIS': brl(INSS_MIS), 'RMT_PRE': brl(RMT_PRE), 'INSS_PRE': brl(INSS_PRE), 'ECON': brl(ECON), 'NOTAS': brl(NOTAS),
        'BARS1': '\n'.join([bar('Custo da obra por aferição', COD, COD), bar('Mão de obra presumida', MO_ALV, COD, small='20% do custo'),
                            bar('Depois do fator social', RMT_ALV, COD, small='40% da mão de obra presumida'), bar('Contribuição', INSS_ALV, COD, 'hl', '36,8% da remuneração')]),
        'BARS2': '\n'.join([bar('Alvenaria, sem planejamento', INSS_ALV, INSS_ALV, 'mute'), bar('Tipo mista', INSS_MIS, INSS_ALV, small='estrutura de metal comprovada por nota'),
                            bar('Pré-fabricado', INSS_PRE, INSS_ALV, 'hl', 'notas de 40% do custo da obra')]),
        'FAQ': '\n'.join('<details><summary>%s</summary><div class="a">%s</div></details>' % (q, a) for q, a in FAQ),
        'IMG': img[0], 'IMGW': str(img[1]), 'IMGH': str(img[2]),
        'URL_IN2021': html.escape(URL_IN2021), 'URL_IN2061': html.escape(URL_IN2061), 'URL_MANUAL': URL_MANUAL, 'URL_SERO': URL_SERO, 'URL_LEI8212': URL_LEI8212, 'URL_CTN': URL_CTN,
    }
    out = _BODY
    for k, v in rep.items(): out = out.replace('[[' + k + ']]', v)
    assert '[[' not in out, re.findall(r'\[\[\w+\]\]', out)
    return out + FAQ_LD

if __name__ == '__main__':
    print(NUM, brl(COD), brl(MO_ALV), brl(RMT_ALV), brl(RMT_PRE), brl(NOTAS), dec(AEQ))
