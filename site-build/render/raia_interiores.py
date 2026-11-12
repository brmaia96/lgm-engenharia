# Casa da Raia: internas na altura do olho (perspectiva, câmera a 1,60 m, vertical reta), montadas com as cotas do executivo.
# Fontes: planta técnica (cotas internas: estar 9,40 x 4,65; suíte 4,80), planta de layout (mobiliário), cortes AA/BB
# (pé-direito 3,30 no estar e cozinha, 2,83 na suíte e banhos; porta de correr 2,50; janela J06 da bancada), quadro de esquadrias
# da Fachada Posterior (porta de correr x 4,39-8,96; janela da suíte x 13,87-15,37, peitoril 1,10, topo 2,10) e quadro de acabamentos.
# Marcenaria e materiais pelas vistas do modelo BIM (cozinha em madeira com aéreos bege e ilha preta, piso em ladrilho
# creme com losango verde, painel ripado de madeira no estar e na cabeceira da suíte). Mesmos eixos do raia_blender.py:
# x ao longo da rua, y da rua para os fundos (piscina), z altura.
# Uso: python -I raia_interiores.py -- VISTA SAIDA W H SPP     (VISTA: cozinha | estar | jantar | suite | planta)
import bpy, bmesh, math, sys, mathutils, random
A = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
VIEW = A[0] if A else 'cozinha'
OUT = A[1] if len(A) > 1 else '/tmp/raia-int.png'
RW, RH, SPP = (int(A[2]), int(A[3]), int(A[4])) if len(A) > 4 else (900, 600, 32)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 8; sc.cycles.diffuse_bounces = 5; sc.cycles.glossy_bounces = 3; sc.cycles.transmission_bounces = 6
sc.cycles.sample_clamp_indirect = 6
sc.render.resolution_x, sc.render.resolution_y = RW, RH
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Base Contrast'; sc.view_settings.exposure = 1.25

def lin(c): return tuple(((v / 255) / 12.92) if v / 255 <= .04045 else (((v / 255 + .055) / 1.055) ** 2.4) for v in c)
def mat(n, c, r=.5, m=0., t=0., ior=1.45):
    M = bpy.data.materials.new(n); M.use_nodes = True; b = M.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*lin(c), 1); b.inputs['Roughness'].default_value = r; b.inputs['Metallic'].default_value = m
    b.inputs['Transmission Weight'].default_value = t; b.inputs['IOR'].default_value = ior; return M
def ruido(M, esc, a, b, bump=.05, det=8, alongar=None):
    nt = M.node_tree; bs = nt.nodes['Principled BSDF']; tx = nt.nodes.new('ShaderNodeTexNoise'); tx.inputs['Scale'].default_value = esc; tx.inputs['Detail'].default_value = det
    if alongar:   # veio de madeira: ruído esticado num eixo
        tc = nt.nodes.new('ShaderNodeNewGeometry'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = alongar
        nt.links.new(tc.outputs['Position'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], tx.inputs['Vector'])
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (*lin(a), 1); cr.color_ramp.elements[1].color = (*lin(b), 1)
    nt.links.new(tx.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], bs.inputs['Base Color'])
    if bump:
        bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = bump; nt.links.new(tx.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], bs.inputs['Normal'])
    return M
def piso_grade(n, base, junta, passo, r=.35, losango=None, passo_y=None, plano='xy'):
    # porcelanato / ladrilho em grade (coordenadas do mundo): junta fina; losango opcional no centro de cada peça
    M = mat(n, base, r); nt = M.node_tree; bs = nt.nodes['Principled BSDF']; N = nt.nodes; L = nt.links.new
    tc = N.new('ShaderNodeNewGeometry'); sp = N.new('ShaderNodeSeparateXYZ'); L(tc.outputs['Position'], sp.inputs['Vector'])
    def f(op, a, b=None, v=None):
        m = N.new('ShaderNodeMath'); m.operation = op
        if hasattr(a, 'bl_idname') or not isinstance(a, (int, float)): L(a, m.inputs[0])
        else: m.inputs[0].default_value = a
        if b is not None:
            if isinstance(b, (int, float)): m.inputs[1].default_value = b
            else: L(b, m.inputs[1])
        return m.outputs[0]
    U, V = {'xy': ('X', 'Y'), 'yz': ('Y', 'Z'), 'xz': ('X', 'Z')}[plano]
    u = f('FRACT', f('DIVIDE', sp.outputs[U], passo)); v = f('FRACT', f('DIVIDE', sp.outputs[V], passo_y or passo))
    ju = f('LESS_THAN', f('ABSOLUTE', f('SUBTRACT', u, .5)), .5 - junta / passo)
    jv = f('LESS_THAN', f('ABSOLUTE', f('SUBTRACT', v, .5)), .5 - junta / (passo_y or passo))
    peca = f('MULTIPLY', ju, jv)
    mix = N.new('ShaderNodeMix'); mix.data_type = 'RGBA'; L(peca, mix.inputs['Factor']); mix.inputs[6].default_value = (*lin(junta_cor), 1); mix.inputs[7].default_value = (*lin(base), 1)
    out = mix.outputs[2]
    if losango:
        d = f('ADD', f('ABSOLUTE', f('SUBTRACT', u, .5)), f('ABSOLUTE', f('SUBTRACT', v, .5)))
        dz = f('LESS_THAN', d, .19)
        m2 = N.new('ShaderNodeMix'); m2.data_type = 'RGBA'; L(dz, m2.inputs['Factor']); L(out, m2.inputs[6]); m2.inputs[7].default_value = (*lin(losango), 1)
        out = m2.outputs[2]
    L(out, bs.inputs['Base Color'])
    bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = .25; bp.inputs['Distance'].default_value = .002; L(peca, bp.inputs['Height']); L(bp.outputs['Normal'], bs.inputs['Normal'])
    return M
junta_cor = (196, 190, 180)

# ---- materiais (quadro de acabamentos + vistas do modelo) ----
pintura = mat('pintura', (240, 238, 233), .9)
forro = mat('forro', (244, 243, 240), .95)
porcelanato = piso_grade('porcelanato-90', (226, 220, 210), .003, .90, .28)
junta_cor = (180, 172, 160)
ladrilho = piso_grade('ladrilho', (234, 226, 208), .003, .20, .45, losango=(52, 86, 76))
junta_cor = (214, 204, 186)
laminado = piso_grade('laminado', (212, 190, 160), .0015, .20, .5, passo_y=1.20)

madeira = ruido(mat('madeira', (122, 80, 54), .45), 3.5, (98, 62, 40), (140, 94, 64), .03, 10, alongar=(1, 1, 14))
madeira_v = ruido(mat('madeira-vert', (110, 72, 48), .5), 3.5, (88, 56, 36), (128, 86, 58), .03, 10, alongar=(1, 1, 14))
bege = mat('laca-bege', (200, 188, 170), .4)
preto = mat('granito-preto', (34, 34, 36), .25)
branco = mat('laca-branca', (236, 235, 232), .35)
inox = mat('inox', (190, 192, 194), .25, 1.)
vidro = mat('vidro', (235, 240, 240), 0., 0., 1., 1.5)
caix = mat('aluminio-preto', (36, 36, 38), .35, .6)
tecido = mat('tecido-claro', (214, 208, 198), .9)
tecido2 = mat('tecido-bege', (196, 184, 166), .9)
tapete = ruido(mat('tapete', (220, 216, 208), .95), 120, (206, 202, 194), (232, 228, 220), .2, 4)
marmore = ruido(mat('marmore', (226, 218, 208), .2), 9, (206, 196, 184), (238, 232, 224), 0, 6)
tv = mat('tela', (12, 12, 14), .08)
folha = mat('folha', (70, 100, 56), .55)
vaso = mat('vaso', (232, 230, 226), .4)
ferro = mat('ferro', (28, 28, 28), .4, .8)
cama = ruido(mat('roupa-de-cama', (240, 238, 234), .9), 40, (232, 230, 226), (246, 244, 240), .1, 3)
couro = mat('estofado-cabeceira', (180, 168, 150), .8)
deck_m = ruido(mat('deck', (206, 200, 188), .6), 25, (196, 190, 178), (214, 208, 196), .08)
grama = ruido(mat('grama', (78, 112, 52), .9), 220, (62, 96, 40), (96, 130, 64), .35, 15)
muro = ruido(mat('muro', (214, 210, 202), .9), 70, (204, 200, 192), (222, 218, 210), .06)
agua = mat('agua', (110, 186, 204), .03)
cerca = ruido(mat('cerca-viva', (58, 92, 40), .8), 14, (40, 70, 28), (86, 124, 56), 1.2, 16)
ladrilho_par = piso_grade('ladrilho-parede', (234, 226, 208), .003, .15, .3, losango=(52, 86, 76), plano='yz')

def box(n, x0, x1, y0, y1, z0, z1, M, bev=0.):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)); o = bpy.context.object
    o.scale = (x1 - x0, y1 - y0, z1 - z0); o.name = n; o.data.materials.append(M)
    if bev:
        bpy.ops.object.transform_apply(scale=True); b = o.modifiers.new('bev', 'BEVEL'); b.width = bev; b.segments = 3
    return o
def cyl(n, x, y, z0, z1, r, M, v=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=z1 - z0, location=(x, y, (z0 + z1) / 2), vertices=v); o = bpy.context.object; o.name = n; o.data.materials.append(M); bpy.ops.object.shade_smooth(); return o
def parede(n, eixo, c0, c1, a0, a1, z1, vaos=(), M=pintura, z0=0.):
    # parede ao longo de x (eixo='x': c0..c1 é y, a0..a1 é x) ou de y; vaos = [(a, b, za, zb)]
    segs = []; cur = a0
    for a, b, za, zb in sorted(vaos):
        if a > cur: segs.append((cur, a, z0, z1))
        if za > z0: segs.append((a, b, z0, za))
        if zb < z1: segs.append((a, b, zb, z1))
        cur = b
    if cur < a1: segs.append((cur, a1, z0, z1))
    for a, b, za, zb in segs:
        if eixo == 'x': box(n, a, b, c0, c1, za, zb, M)
        else: box(n, c0, c1, a, b, za, zb, M)
def esquadria_x(x0, x1, z0, z1, y, folhas):
    box('vidro', x0, x1, y - .006, y + .006, z0, z1, vidro)
    t = .05
    for a, b, c, d in ((x0, x1, z0, z0 + t), (x0, x1, z1 - t, z1), (x0, x0 + t, z0, z1), (x1 - t, x1, z0, z1)): box('caix', a, b, y - .03, y + .03, c, d, caix)
    for k in range(1, folhas): xm = x0 + (x1 - x0) * k / folhas; box('caix', xm - .025, xm + .025, y - .03, y + .03, z0, z1, caix)
def esquadria_y(y0, y1, z0, z1, x, folhas):
    box('vidro', x - .006, x + .006, y0, y1, z0, z1, vidro)
    t = .05
    for a, b, c, d in ((y0, y1, z0, z0 + t), (y0, y1, z1 - t, z1), (y0, y0 + t, z0, z1), (y1 - t, y1, z0, z1)): box('caix', x - .03, x + .03, a, b, c, d, caix)
    for k in range(1, folhas): ym = y0 + (y1 - y0) * k / folhas; box('caix', x - .03, x + .03, ym - .025, ym + .025, z0, z1, caix)
def ripado(eixo, c, a0, a1, z0, z1, M=madeira_v, passo=.07, larg=.04, prof=.03, lado=1):
    # painel de ripas verticais sobre fundo escuro; c = face da parede, lado = para onde o painel avança
    fundo = mat('fundo-ripado', (52, 36, 26), .7)
    if eixo == 'x': box('fundo-rip', a0, a1, c, c + lado * .012, z0, z1, fundo)
    else: box('fundo-rip', c, c + lado * .012, a0, a1, z0, z1, fundo)
    a = a0 + .01
    while a + larg <= a1:
        if eixo == 'x': box('ripa', a, a + larg, min(c + lado * .012, c + lado * (.012 + prof)), max(c + lado * .012, c + lado * (.012 + prof)), z0, z1, M)
        else: box('ripa', min(c + lado * .012, c + lado * (.012 + prof)), max(c + lado * .012, c + lado * (.012 + prof)), a, a + larg, z0, z1, M)
        a += passo

# ======================= ÁREA SOCIAL (cozinha / estar / jantar) =======================
# interno: x 3,36-12,76 (9,40); y 8,26-12,91 (4,65); pé-direito 3,30 sob forro
X0, X1, Y0, Y1, PD = 3.36, 12.76, 8.26, 12.91, 3.30
box('piso-porcelanato', X0, X1, Y0, Y1, -.02, 0, porcelanato)
box('piso-ladrilho', X0, 6.80, Y0, Y1, -.02, .002, ladrilho)          # cozinha: ladrilho do modelo (x 3,36-6,80)
box('forro', X0 - .2, X1 + .2, Y0 - .2, Y1 + .2, PD, PD + .05, forro)
# parede norte (fundos): porta de correr de quatro folhas x 4,39-8,96 até 2,50; passagem para o lavabo e banho social x 9,95-10,80
parede('n', 'x', Y1, Y1 + .15, X0 - .15, X1 + .15, PD, [(4.39, 8.96, 0, 2.50), (9.95, 10.80, 0, 2.40)])
esquadria_x(4.39, 8.96, 0, 2.50, Y1 + .075, 4)
# hall do lavabo e banho social atrás da passagem (fechado, portas de madeira)
box('hall-lav-fundo', 9.06, 12.76, 13.95, 14.10, 0, 2.83, pintura); box('hall-lav-forro', 9.06, 12.76, Y1 + .15, 14.0, 2.83, 2.88, forro)
box('hall-lav-piso', 9.06, 12.76, Y1, 14.0, -.02, 0, porcelanato)
box('hall-lav-e', 9.06, 9.21, Y1, 14.0, 0, 2.83, pintura); box('hall-lav-d', 12.61, 12.76, Y1, 14.0, 0, 2.83, pintura)
# parede oeste: janela J06 sobre a bancada (2,50 de largura; 1,05 do canto norte), peitoril 1,15, topo 1,62 (corte BB)
JY0, JY1 = Y1 - 1.05 - 2.50, Y1 - 1.05
parede('o', 'y', X0 - .15, X0, Y0 - .15, Y1 + .15, PD, [(JY0, JY1, 1.15, 1.62)])
esquadria_y(JY0, JY1, 1.15, 1.62, X0 - .075, 2)
# parede sul: porta da despensa (madeira, fechada) x 4,05-4,85; passagem para o hall de entrada x 6,05-7,70
parede('s', 'x', Y0 - .15, Y0, X0 - .15, X1 + .15, PD, [(4.05, 4.85, 0, 2.10), (6.05, 7.70, 0, 2.40)])
box('porta-despensa', 4.05, 4.85, Y0 - .10, Y0 - .06, 0, 2.10, madeira)
box('hall-fundo', 6.05, 7.70, 6.90, 7.05, 0, PD, pintura); box('hall-piso', 6.05, 7.70, 6.95, Y0, -.02, 0, porcelanato)
box('hall-e', 5.90, 6.05, 6.95, Y0, 0, PD, pintura); box('hall-d', 7.70, 7.85, 6.95, Y0, 0, PD, pintura); box('hall-forro', 5.9, 7.85, 6.9, Y0, 2.83, 2.88, forro)
box('sapateira', 6.10, 7.65, 7.05, 7.45, 0, .85, madeira)       # "sapateira + quadros" da planta de layout
# parede leste: painel da TV; vão V01 para a circulação y 8,26-9,75
parede('l', 'y', X1, X1 + .15, Y0 - .15, Y1 + .15, PD, [(Y0, 9.75, 0, 2.40)])
box('circ-fundo', 14.95, 15.10, 7.9, 10.0, 0, 2.83, pintura); box('circ-piso', X1, 15.0, 7.9, 10.0, -.02, 0, porcelanato)
box('circ-forro', X1, 15.1, 7.9, 10.0, 2.83, 2.88, forro); box('circ-s', X1, 15.1, 7.75, 7.90, 0, 2.83, pintura)
box('porta-suite', 14.25, 14.95, 9.98, 10.02, 0, 2.10, madeira)
# rodapé do mesmo porcelanato, h = 10 cm
for a in ((X0, X1, Y0, Y0 + .012), (X0, X1, Y1 - .012, Y1)): box('rodape', a[0], a[1], a[2], a[3], 0, .10, mat('rodape', (222, 216, 206), .3))

# ---- cozinha (parede oeste, x 3,36-3,96) ----
CF = X0 + .60
box('torre-forno', X0, CF, Y0, Y0 + .75, 0, 2.30, madeira)                          # torre quente na ponta sul (corte BB)
box('micro', CF - .01, CF + .003, Y0 + .12, Y0 + .63, 1.40, 1.75, tv); box('forno', CF - .01, CF + .003, Y0 + .12, Y0 + .63, .80, 1.38, tv)
box('base', X0, CF, Y0 + .75, 12.10, 0, .86, madeira)
for y in (9.40, 9.95, 10.50, 11.05):
    box('puxador', CF, CF + .015, y - .20, y + .20, .74, .75, inox)
box('tampo', X0, CF + .02, Y0 + .75, 12.10, .86, .90, preto)
box('lava-louca', CF, CF + .003, 11.30, 11.90, .10, .82, tv)                          # lava-louças embutida
box('cuba', X0 + .12, X0 + .50, JY0 + 1.05, JY0 + 1.65, .70, .905, inox)
cyl('torneira', X0 + .08, JY0 + 1.35, .90, 1.22, .015, inox); box('bica', X0 + .06, X0 + .30, JY0 + 1.34, JY0 + 1.36, 1.20, 1.22, inox)
for a, b, c, d in ((Y0 + .75, 12.10, .90, 1.15), (Y0 + .75, JY0, 1.15, 1.68), (JY1, 12.10, 1.15, 1.68), (JY0, JY1, 1.62, 1.68)):
    box('revestimento', X0, X0 + .006, a, b, c, d, ladrilho_par)        # revestimento entre bancada e armários, em volta da J06
box('aereos', X0, X0 + .35, Y0 + .75, 12.10, 1.68, 2.30, bege)
for k in range(6):
    y = Y0 + .75 + (12.10 - Y0 - .75) * k / 6
    box('junta-aereo', X0 + .348, X0 + .352, y - .003, y + .003, 1.68, 2.30, mat('sombra', (120, 112, 100), .6))
# torre da churrasqueira na ponta norte (chaminé circular da planta), revestida em madeira e aço até o forro
box('torre-churr', X0, X0 + .70, 12.10, Y1, 0, PD, madeira)
box('chapa-churr', X0 + .69, X0 + .705, 12.10, Y1, 1.75, PD, mat('aco-escovado', (128, 128, 130), .35, .9))
box('boca-churr', X0 + .30, X0 + .706, 12.22, Y1 - .12, .95, 1.55, ferro)
for k in range(6): box('espeto', X0 + .32, X0 + .70, 12.28 + k * .11, 12.29 + k * .11, 1.12, 1.13, inox)
# geladeira na parede sul (REF), em torre de madeira, porta inox para a ilha
box('torre-ref', 4.92, 6.05, Y0, Y0 + .72, 0, 2.30, madeira)
box('ref-inox', 5.00, 5.97, Y0 + .70, Y0 + .73, .05, 1.85, inox)
box('ref-vinco', 5.48, 5.49, Y0 + .73, Y0 + .735, .05, 1.85, tv)
# ilha: x 5,08-6,24, y 9,30-12,42; corpo branco, tampo preto com lateral em cascata na ponta norte; cooktop no meio
box('ilha', 5.12, 6.20, 9.30, 12.30, 0, .88, branco)
box('ilha-tampo', 5.08, 6.24, 9.30, 12.42, .88, .92, preto)
box('ilha-cascata', 5.08, 6.24, 12.38, 12.42, 0, .92, preto)
box('cooktop', 5.30, 6.02, 10.50, 11.25, .92, .925, tv)
for x, y in ((5.48, 10.68), (5.84, 10.68), (5.48, 11.07), (5.84, 11.07)): cyl('boca', x, y, .925, .927, .09, mat('aro', (60, 60, 62), .3, .5))
for y in (9.85, 10.85, 11.85):      # três pendentes pretos sobre a ilha (corte BB)
    cyl('fio', 5.66, y, 2.00, PD, .004, ferro); cyl('pendente', 5.66, y, 1.75, 2.00, .09, ferro)
    bpy.ops.object.light_add(type='POINT', location=(5.66, y, 1.73)); L = bpy.context.object; L.data.energy = 18; L.data.color = (1., .85, .68); L.data.shadow_soft_size = .05

# ---- jantar: mesa x 7,95-8,99, y 9,80-12,30; oito cadeiras ----
box('mesa-tampo', 7.95, 8.99, 9.80, 12.30, .72, .76, madeira, .005)
for x, y in ((8.05, 9.95), (8.89, 9.95), (8.05, 12.15), (8.89, 12.15)): box('mesa-pe', x - .03, x + .03, y - .03, y + .03, 0, .72, madeira)
def cadeira(x, y, ang):
    g = []
    g.append(box('assento', -.24, .24, -.24, .24, .44, .52, tecido2, .02))
    g.append(box('encosto', -.24, .24, .20, .27, .52, 1.02, tecido2, .03))
    for a, b in ((-.2, -.2), (.2, -.2), (-.2, .22), (.2, .22)): g.append(box('perna', a - .015, a + .015, b - .015, b + .015, 0, .44, madeira))
    e = bpy.data.objects.new('cadeira', None); bpy.context.collection.objects.link(e)
    for o in g: o.parent = e
    e.location = (x, y, 0); e.rotation_euler = (0, 0, ang)
for y in (10.35, 11.05, 11.75):
    cadeira(7.62, y, math.radians(-90)); cadeira(9.32, y, math.radians(90))
cadeira(8.47, 9.42, 0); cadeira(8.47, 12.68, math.radians(180))
box('pendente-linear', 8.40, 8.54, 10.30, 11.80, 1.62, 1.66, ferro)
for y in (10.4, 11.7): cyl('fio', 8.47, y, 1.66, PD, .003, ferro)
bpy.ops.object.light_add(type='AREA', location=(8.47, 11.05, 1.61)); L = bpy.context.object; L.data.shape = 'RECTANGLE'; L.data.size = .10; L.data.size_y = 1.4
L.rotation_euler = (math.pi, 0, 0); L.data.energy = 40; L.data.color = (1., .86, .7)

# ---- estar: tapete, sofá curvo voltado para a TV, mesa de centro, poltrona, planta ----
box('tapete', 10.40, 12.40, 9.85, 12.75, 0, .012, tapete)
# sofá: corpo, encosto curvo (arco), almofadas
box('sofa-base', 10.35, 11.20, 9.95, 12.25, .10, .42, tecido, .04)
for y in (10.35, 11.10, 11.85): box('almofada', 10.62, 11.15, y - .36, y + .36, .42, .56, tecido, .05)
cu = bpy.data.curves.new('sofa-encosto', 'CURVE'); cu.dimensions = '3D'; sp_ = cu.splines.new('POLY'); N_ = 24; sp_.points.add(N_ - 1)
for k in range(N_):
    tt = math.pi / 2 + math.pi * k / (N_ - 1); sp_.points[k].co = (10.82 + .44 * math.cos(tt), 11.10 + 1.20 * math.sin(tt), .58, 1)
cu.bevel_depth = .10; cu.bevel_resolution = 4; cu.extrude = .18; cu.use_fill_caps = True
o = bpy.data.objects.new('sofa-encosto', cu); bpy.context.collection.objects.link(o); cu.materials.append(tecido)
for x, y in ((10.42, 10.02), (10.42, 12.18), (11.12, 10.02), (11.12, 12.18)): box('pe-sofa', x - .02, x + .02, y - .02, y + .02, 0, .10, madeira)
cyl('mesa-centro', 11.62, 11.30, .40, .43, .42, marmore, 48); cyl('mesa-centro-pe', 11.62, 11.30, 0, .40, .03, ferro)
box('livros', 11.50, 11.78, 11.22, 11.42, .43, .48, mat('livro', (160, 150, 136), .7))
# poltrona (x 11,2-12,2, y 9,3-10,2), estrutura de madeira e almofadas claras, voltada para o sofá/TV
e = bpy.data.objects.new('poltrona', None); bpy.context.collection.objects.link(e)
for o in (box('pol-assento', -.36, .36, -.38, .30, .36, .48, tecido, .04), box('pol-encosto', -.36, .36, .26, .36, .42, .92, tecido, .04),
          box('pol-braco-e', -.40, -.36, -.40, .36, .55, .58, madeira), box('pol-braco-d', .36, .40, -.40, .36, .55, .58, madeira)):
    o.parent = e
for a, b in ((-.38, -.38), (.38, -.38), (-.38, .34), (.38, .34)):
    o = box('pol-perna', a - .02, a + .02, b - .02, b + .02, 0, .58, madeira); o.parent = e
e.location = (11.75, 9.62, 0); e.rotation_euler = (0, 0, math.radians(200))
# painel ripado de madeira na parede leste, rack bege suspenso, prateleira e TV
ripado('y', X1, 9.95, Y1, 0, PD, lado=-1)
box('rack', X1 - .45, X1 - .045, 10.10, 12.80, .25, .70, bege)
for y in (11.00, 11.90): box('junta-rack', X1 - .452, X1 - .448, y - .003, y + .003, .25, .70, mat('sombra2', (130, 120, 108), .6))
box('prateleira', X1 - .32, X1 - .045, 10.30, 12.60, 2.30, 2.34, bege)
box('tv', X1 - .09, X1 - .05, 10.73, 12.17, 1.00, 1.83, tv)
cyl('vaso-planta', 9.62, 12.55, 0, .45, .24, vaso, 40)
random.seed(7)
for k in range(9):    # folhas largas (estrelítzia / ave-do-paraíso) em hastes
    a = k * 2.4; h = 1.0 + .5 * random.random()
    cyl('haste', 9.62 + .05 * math.cos(a), 12.55 + .05 * math.sin(a), .4, h, .008, folha)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=1, location=(9.62 + .20 * math.cos(a), 12.55 + .20 * math.sin(a), h + .14)); o = bpy.context.object
    o.scale = (.012, .12, .30); o.rotation_euler = (math.radians(25 + 20 * random.random()), 0, a); o.data.materials.append(folha); bpy.ops.object.shade_smooth()
# iluminação embutida no forro (spots), quente e fraca
for x in (4.6, 7.0, 9.6, 11.6):
    for y in (9.2, 11.9):
        bpy.ops.object.light_add(type='SPOT', location=(x, y, PD - .01)); L = bpy.context.object; L.data.energy = 25; L.data.spot_size = math.radians(70)
        L.data.spot_blend = .6; L.data.color = (1., .87, .72); L.data.shadow_soft_size = .03
        box('spot', x - .05, x + .05, y - .05, y + .05, PD - .004, PD, mat('aro-spot', (60, 60, 60), .4))

# ======================= SUÍTE =======================
# interno x 12,91-17,71 (4,80); y 11,45 (parede do banho 03, cabeceira) a 14,26 (parede norte); armário na parede oeste
# de y 9,85 a 14,26; corredor de acesso entre o armário e o banho 03 (x 13,56-15,08); pé-direito 2,83
SX0, SX1, SY0, SY1, SP = 12.91, 17.71, 11.45, 14.26, 2.83
box('piso-laminado', SX0, SX1, 9.85, SY1, -.02, 0, laminado)
box('forro-suite', SX0 - .1, SX1 + .1, 9.70, SY1 + .1, SP, SP + .05, forro)
parede('sn', 'x', SY1, SY1 + .15, SX0 - .15, SX1 + .15, SP, [(13.87, 15.37, 1.10, 2.10)])
esquadria_x(13.87, 15.37, 1.10, 2.10, SY1 + .075, 2)
parede('sl', 'y', SX1, SX1 + .15, SY0 - .15, SY1 + .15, SP)
box('so', SX0 - .15, SX0, 9.70, SY1 + .15, 0, SP, pintura)
box('banho3-n', 15.08, SX1, SY0 - .15, SY0, 0, SP, pintura); box('banho3-o', 14.93, 15.08, 9.70, SY0, 0, SP, pintura)
parede('circ-n', 'x', 9.70, 9.85, SX0, 14.93, SP, [(14.20, 14.93, 0, 2.10)])
box('porta-suite-aberta', 14.20, 14.24, 9.10, 9.85, 0, 2.10, madeira)
# armário: portas de correr brancas com nicho bege no alto e lateral de madeira (vista do modelo)
AF = SX0 + .62
box('armario', SX0, AF, 9.85, SY1, 0, 2.30, branco)
box('armario-topo', SX0, AF, 9.85, SY1, 2.30, SP, bege)
for k in range(1, 4):
    y = 9.85 + (SY1 - 9.85) * k / 4
    box('junta-armario', AF, AF + .004, y - .004, y + .004, .02, 2.28, mat('sombra3', (150, 148, 144), .6))
box('armario-lat', SX0, AF + .02, SY1 - .02, SY1, 0, SP, madeira)
# cabeceira: painel ripado de madeira do piso ao forro e cabeceira estofada; cama de casal 1,96 x 2,04
ripado('x', SY0, 15.08, SX1, 0, SP, lado=1)
box('cabeceira', 15.50, 17.66, SY0 + .05, SY0 + .13, .30, 1.25, couro, .02)
for k in range(1, 6): x = 15.50 + 2.16 * k / 6; box('gomo', x - .004, x + .004, SY0 + .13, SY0 + .135, .32, 1.23, mat('sombra4', (140, 128, 112), .7))
box('cama-base', 15.62, 17.58, SY0 + .13, SY0 + 2.17, .12, .40, mat('cama-base', (64, 64, 66), .7))
box('colchao', 15.66, 17.54, SY0 + .15, SY0 + 2.12, .40, .64, cama, .06)
for x in (16.08, 17.12): box('travesseiro', x - .36, x + .36, SY0 + .18, SY0 + .62, .64, .76, cama, .04)
for x in (16.20, 17.00): box('almofada-cama', x - .26, x + .26, SY0 + .55, SY0 + .70, .64, .98, mat('almofada-bege', (196, 182, 160), .9), .05)
box('peseira', 15.64, 17.56, SY0 + 1.55, SY0 + 2.14, .64, .68, mat('manta', (176, 162, 142), .9), .03)
box('criado', 15.12, 15.52, SY0 + .05, SY0 + .45, 0, .52, bege)
# bancada preta baixa junto à parede norte com a TV (vista do modelo e planta de layout)
box('bancada-tv', 15.50, 17.66, SY1 - .40, SY1, 0, .45, mat('laca-preta', (30, 30, 32), .35))
box('tv-suite', 16.08, 17.08, SY1 - .25, SY1 - .21, .52, 1.12, tv); box('tv-pe', 16.50, 16.66, SY1 - .30, SY1 - .16, .45, .52, ferro)
box('rodape-suite', SX0, SX1, SY1 - .012, SY1, 0, .10, pintura)
for x, y in ((14.2, 13.3), (16.6, 12.0), (16.6, 13.6)):
    bpy.ops.object.light_add(type='SPOT', location=(x, y, SP - .01)); L = bpy.context.object; L.data.energy = 14; L.data.spot_size = math.radians(70)
    L.data.spot_blend = .6; L.data.color = (1., .86, .7); L.data.shadow_soft_size = .03

# ======================= exterior visto pelas esquadrias =======================
box('deck', -2, 22, Y1, 16.65, -.05, -.02, deck_m)
box('grama', -2, 22, 16.65, 16.9, -.05, -.01, grama); box('borda', 1.15, 19.65, 16.65, 16.90, -.05, .02, deck_m)
box('agua', 1.40, 19.40, 16.90, 19.16, -.10, -.04, agua); box('borda-t', 1.15, 19.65, 19.16, 19.35, -.05, .02, deck_m)
box('muro-fundo', -2, 22, 19.85, 20.0, -.05, 2.2, muro); box('muro-oeste', 0, .15, 0, 20, -.05, 2.2, muro)
box('chao-oeste', -2, X0 - .15, 0, 20, -.05, -.02, deck_m)
random.seed(4)
for k in range(12):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=.8, location=(2.8 + k * 1.4, 19.5, .85)); o = bpy.context.object
    o.scale = (.95, .45, 1.15); o.data.materials.append(cerca)
    d = o.modifiers.new('disp', 'DISPLACE'); t = bpy.data.textures.new('cv%d' % k, 'VORONOI'); t.noise_scale = .09; d.texture = t; d.strength = .12
# cobertura de vidro retrátil a oeste (x 0,15-2,25), vista pela janela da bancada
box('vidro-cob', .15, 2.25, 7.25, 11.87, 3.14, 3.17, vidro)
for y in (7.25, 8.79, 10.33, 11.87): box('perfil', .15, 2.25, y - .04, y + .04, 3.12, 3.2, caix)

box('beiral', 2.25, 19.0, 12.93, 14.50, 2.98, 3.45, mat('telha-sob', (150, 120, 100), .8))
box('beiral-forro', 2.25, 19.0, 13.06, 14.50, 2.96, 2.98, mat('beiral-madeira', (120, 86, 60), .6))
# ---- céu e sol (manhã clara; o sol entra pelas esquadrias do lado da piscina) ----
w = bpy.data.worlds.new('ceu'); sc.world = w; w.use_nodes = True; nw = w.node_tree
sky = nw.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'NISHITA'; sky.sun_disc = False; sky.sun_elevation = math.radians(38); sky.sun_rotation = math.radians(290)
nw.nodes['Background'].inputs['Strength'].default_value = .6; nw.links.new(sky.outputs['Color'], nw.nodes['Background'].inputs['Color'])
bpy.ops.object.light_add(type='SUN'); sun = bpy.context.object; sun.data.energy = 4.5; sun.data.angle = math.radians(1.5); sun.data.color = (1., .95, .88)
trav = mathutils.Vector((.40, -.75, -.52)).normalized(); sun.rotation_euler = trav.to_track_quat('-Z', 'Y').to_euler()
# portais de luz nas esquadrias (só amostragem; não aparecem)
for (x0, x1, y, z0, z1) in ((4.39, 8.96, Y1 + .2, 0, 2.5), (13.87, 15.37, SY1 + .2, 1.1, 2.1)):
    bpy.ops.object.light_add(type='AREA', location=((x0 + x1) / 2, y, (z0 + z1) / 2)); L = bpy.context.object; L.data.shape = 'RECTANGLE'
    L.data.size = x1 - x0; L.data.size_y = z1 - z0; L.rotation_euler = (math.radians(-90), 0, 0); L.data.cycles.is_portal = True
bpy.ops.object.light_add(type='AREA', location=(X0 - .3, (JY0 + JY1) / 2, 1.385)); L = bpy.context.object; L.data.shape = 'RECTANGLE'
L.data.size = .47; L.data.size_y = 2.5; L.rotation_euler = (0, math.radians(90), 0); L.data.cycles.is_portal = True

# ---- câmeras (altura do olho 1,60 m, horizonte reto: inclinação zero, enquadramento por shift) ----
CAMS = {
    # cozinha: do estar, olhando para a parede oeste (bancada sob a janela, ilha à frente, churrasqueira à direita, torre quente à esquerda)
    'cozinha': ((8.55, 12.55), (3.4, 9.7), 22, -.06),
    # estar e TV: do canto noroeste do jantar, olhando para o painel ripado da parede leste
    'estar': ((9.45, 8.65), (12.7, 12.1), 24, -.05),
    # jantar e estar: da ponta sul da ilha, olhando a mesa, a porta de correr à esquerda e o estar ao fundo
    'jantar': ((6.60, 8.85), (11.2, 12.4), 24, -.05),
    # suíte: do corredor do armário, olhando a cama com a cabeceira ripada à direita e a janela à esquerda
    'suite': ((13.85, 12.30), (17.7, 12.75), 21, -.06),
}
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam; cam.data.sensor_width = 36
if VIEW == 'planta':        # conferência: vista de cima ortogonal, sem forro
    for o in bpy.data.objects:
        if o.name.startswith(('forro', 'hall-lav-forro', 'hall-forro', 'circ-forro', 'vidro-cob', 'perfil')): o.hide_render = True
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = 15.5; cam.location = (10.5, 11.0, 30); cam.rotation_euler = (0, 0, 0)
    sun.rotation_euler = (0, 0, 0); sun.data.energy = 2
else:
    (cx, cy), (tx, ty), f, sh = CAMS[VIEW]
    cam.location = (cx, cy, 1.60); cam.data.lens = f
    if VIEW == 'suite': sc.view_settings.exposure = 1.75
    yaw = math.atan2(ty - cy, tx - cx) - math.pi / 2
    cam.rotation_euler = (math.radians(90), 0, yaw); cam.data.shift_y = sh
    cam.data.clip_start = .05
sc.render.filepath = OUT; bpy.ops.render.render(write_still=True); print('ok', OUT)
