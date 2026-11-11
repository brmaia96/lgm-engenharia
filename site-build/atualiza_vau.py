# -*- coding: utf-8 -*-
"""Troca o VAU do mês nas páginas já montadas, sem refazer o site (não precisa das imagens de origem).

O VAU da Receita muda todo mês: sobe pela variação do Sinapi e é revisto em janeiro.
Passos:
  1. Atualize `vau_uf.json`: "mes" (AAAA-MM), "rotulo" ("dezembro de 2026") e os 27 valores de "ufs"
     (residencial unifamiliar). A tabela oficial fica no Sero (e-CAC > Aferições > Consultar Tabela VAU).
  2. Rode:  python3 atualiza_vau.py
  3. Publique `site/inss.html` e `site/index.html` (na página publicada como Artifact, a home tem outro
     invólucro: aplique lá a mesma troca do número do exemplo).

O script confere se cada troca aconteceu exatamente uma vez e falha sem gravar nada se a página mudou de forma.
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site')

spec = importlib.util.spec_from_file_location('inss_page', os.path.join(HERE, 'inss_page.py'))
N = importlib.util.module_from_spec(spec); spec.loader.exec_module(N)   # lê vau_uf.json e recalcula o exemplo

if len(N.VAU_UF) != 27:
    sys.exit('vau_uf.json precisa ter os 27 estados com valor; tem %d.' % len(N.VAU_UF))
if any(not (1000 < v < 8000) for v in N.VAU_UF.values()):
    sys.exit('Há valor de VAU fora da faixa esperada (R$ 1.000 a R$ 8.000 por m²). Confira o arquivo.')

def troca(texto, padrao, novo, nome):
    out, n = re.subn(padrao, novo, texto, flags=re.S)
    if n != 1:
        sys.exit('Não gravei nada: esperava achar "%s" uma vez e achei %d. A página mudou; refaça pelo build.py.' % (nome, n))
    return out

sem, econ, rotulo = N.NUM['sem'], N.NUM['econ'], N.VAUS['rotulo']
vau_js = json.dumps({k: round(v, 2) for k, v in N.VAU_UF.items()})

p_inss = os.path.join(SITE, 'inss.html'); inss = open(p_inss, encoding='utf-8').read()
inss = troca(inss, r'var VAU=\{[^}]*\}', lambda m: 'var VAU=' + vau_js, 'tabela VAU do script')
inss = troca(inss, r'(valor por metro quadrado de )[^.<]+', lambda m: m.group(1) + rotulo, 'mês de referência')
inss = troca(inss, r'(id="v-sem">)[^<]*', lambda m: m.group(1) + sem, 'valor inicial sem planejamento')
inss = troca(inss, r'(id="v-eco">)[^<]*', lambda m: m.group(1) + 'até ' + econ, 'valor inicial da redução')

p_home = os.path.join(SITE, 'index.html'); home = open(p_home, encoding='utf-8').read()
home = troca(home, r'(<div class="num">)[^<]*(</div><div class="nl">de INSS em uma casa de)', lambda m: m.group(1) + sem + m.group(2), 'número do exemplo na home')

open(p_inss, 'w', encoding='utf-8').write(inss)
open(p_home, 'w', encoding='utf-8').write(home)
print('VAU de %s aplicado. Exemplo da home: casa de %s em %s, %s sem planejamento.' % (rotulo, N.NUM['area'], N.NUM['uf'], sem.replace(' ', ' ')))
