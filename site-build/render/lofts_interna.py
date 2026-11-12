# Le Blanc Lofts, interior de um loft: montado SÓ com as cotas da Planta Baixa Térreo (P01) e do Corte BB (P02).
# Planta: x da face externa oeste (0) para a leste (4,55); y da face externa da fachada (0) para os fundos (5,65); paredes de 0,15.
# Níveis do corte BB: térreo +0,15; patamar +0,84; forro sob o mezanino +2,55 (laje 2,65-2,90); mezanino +2,90; forro alto +5,30.
# Mezanino (corte BB): laje dos fundos até 3,15 da face de fundo (y 2,50), guarda-corpo de vidro com montantes.
# Escada: degraus 1-4 junto à fachada (x 1,05-2,21), patamar 0,90 x 0,90 no canto, lance 5-16 junto à parede oeste (x 0,15-1,05,
# piso 0,29, espelho ~0,172) até o mezanino. Esquadrias do quadro (P01): P01 pivotante 1,20 x 2,20 (x 2,17-3,37); J01 1,00 x 0,40;
# J02 0,60 x 0,60; J03 1,50 x 0,40 sobre a pia; J04 0,30 x 4,40 junto ao patamar; J05 2,00 x 0,60 no mezanino.
# Layout da planta: bancada da cozinha na parede leste com cooktop e pia, geladeira, área de serviço, sofá e rack junto ao banheiro.
# Acabamentos: a prancha não define; neutros (branco gelo, porcelanato claro, madeira clara, metal grafite).
import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'int_lib.py')).read())
W, D = 4.55, 5.65; P = .15; FL = .15; MZ = 2.90; MZB = 2.65; FORRO_B = 2.55; FORRO_A = 5.30; TOPO = 5.45
gelo = mat('gelo', (236, 234, 229), .9); ruido(gelo, 80, (230, 228, 223), (240, 238, 233), .02)
piso = mat('porcelanato', (205, 200, 191), .35); piso_placas(piso, .90, (206, 201, 192), (199, 194, 185))
madeira = mat('madeira', (176, 140, 102), .55); veio(madeira, 3, (160, 124, 88), (186, 150, 112))
porta_m = mat('porta-madeira', (120, 88, 60), .5); veio(porta_m, 3, (108, 78, 52), (132, 98, 68))
grafite = mat('grafite', (52, 52, 54), .4, .8)
inox = mat('inox', (190, 190, 188), .25, 1.)
pedra = mat('bancada', (226, 222, 214), .25); ruido(pedra, 30, (218, 214, 206), (232, 228, 220), .01)
marc_b = mat('marcenaria', (222, 218, 210), .45)
tecido = mat('tecido', (176, 168, 156), .9); ruido(tecido, 200, (168, 160, 148), (184, 176, 164), .2)
preto = mat('preto', (22, 22, 24), .3)
chao_ext = mat('externo', (190, 186, 178), .85)
# piso e entorno
box('piso', P, W - P, P, D - P, FL - .02, FL, piso)
box('ext', -20, 25, -20, 25, -.02, 0, chao_ext)
box('laje-teto', -.05, W + .05, -.05, D + .05, TOPO, TOPO + .1, gelo)
box('forro-alto', P, W - P, P, D - P, FORRO_A, FORRO_A + .02, gelo)
# paredes externas com os vãos (u ao longo da parede, z absoluto)
parede('frente', 'x', 0, P, 0, W, 0, TOPO, gelo, [(2.17, 3.37, FL, 2.35)])
parede('fundos', 'x', D - P, D, 0, W, 0, TOPO, gelo, [(2.80, 3.80, 1.55, 1.95), (1.35, 3.35, 4.40, 5.00)])
parede('oeste', 'y', 0, P, P, D - P, 0, TOPO, gelo, [(.40, .70, .90, 5.30), (4.55, 5.15, 1.70, 2.30)])
parede('leste', 'y', W - P, W, P, D - P, 0, TOPO, gelo, [(1.17, 2.67, 1.50, 1.90)])
janela('x', D - P / 2, 2.80, 3.80, 1.55, 1.95); janela('x', D - P / 2, 1.35, 3.35, 4.40, 5.00)
janela('y', P / 2, .40, .70, .90, 5.30, 1); janela('y', P / 2, 4.55, 5.15, 1.70, 2.30, 1); janela('y', W - P / 2, 1.17, 2.67, 1.50, 1.90)
portal('y', 0, .40, .70, .90, 5.30, -1); portal('y', W, 1.17, 2.67, 1.50, 1.90, 1)
portal('x', D, 1.35, 3.35, 4.40, 5.00, 1); portal('x', D, 2.80, 3.80, 1.55, 1.95, 1)
# porta pivotante P01 fechada (vista de dentro)
box('batente', 2.13, 2.17, 0, P, FL, 2.39, grafite); box('batente', 3.37, 3.41, 0, P, FL, 2.39, grafite); box('batente', 2.13, 3.41, 0, P, 2.35, 2.39, grafite)
box('folha-P01', 2.17, 3.37, .06, .11, FL + .01, 2.35, porta_m); box('puxador', 2.36, 2.39, .11, .15, .55, 1.95, inox)
# mezanino: laje dos fundos (y 2,50 a 5,50) entre a escada e a parede leste; patamar de chegada sobre o lance
box('laje-mez', 1.05, W - P, 2.50, D - P, MZB, MZ, gelo)
box('laje-mez-cheg', P, 1.05, 4.54, D - P, MZB, MZ, gelo)
box('forro-baixo', 1.05, W - P, 2.52, D - P, FORRO_B, FORRO_B + .02, gelo); box('forro-baixo2', P, 1.05, 4.54, D - P, FORRO_B, FORRO_B + .02, gelo)
box('piso-mez', 1.05, W - P, 2.50, D - P, MZ - .01, MZ, madeira); box('piso-mez2', P, 1.05, 4.54, D - P, MZ - .01, MZ, madeira)
vgc = mat('vidro-gc', (225, 235, 232), .02, 0., trans=1.)
def guarda(eixo, c, a, b):
    if eixo == 'x':
        box('gc-vidro', a, b, c - .006, c + .006, MZ + .05, MZ + 1.05, vgc); box('gc-corrimao', a, b, c - .025, c + .025, MZ + 1.05, MZ + 1.10, grafite)
        n = max(1, round((b - a) / 1.1)); [box('gc-mont', a + (b - a) * k / n - .02, a + (b - a) * k / n + .02, c - .03, c + .03, MZ, MZ + 1.10, grafite) for k in range(n + 1)]
    else:
        box('gc-vidro', c - .006, c + .006, a, b, MZ + .05, MZ + 1.05, vgc); box('gc-corrimao', c - .025, c + .025, a, b, MZ + 1.05, MZ + 1.10, grafite)
        n = max(1, round((b - a) / 1.1)); [box('gc-mont', c - .03, c + .03, a + (b - a) * k / n - .02, a + (b - a) * k / n + .02, MZ, MZ + 1.10, grafite) for k in range(n + 1)]
guarda('x', 2.50, 1.05, W - P); guarda('y', 1.05, 2.50, 4.40)
# escada: degraus 1-4 e patamar (+0,84), lance 5-16 em laje inclinada
E = (MZ - .84) / 12
for k, (x0, x1) in enumerate(((1.92, 2.21), (1.63, 1.92), (1.34, 1.63), (1.05, 1.34))):
    zt = FL + (k + 1) * (.84 - FL) / 4
    box('degrau%d' % (k + 1), x0, x1, P, 1.05, FL, zt - .03, gelo); box('piso-degrau', x0 - .02, x1, P, 1.07, zt - .03, zt, madeira)
box('patamar', P, 1.05, P, 1.06, FL, .81, gelo); box('piso-patamar', P, 1.07, P, 1.08, .81, .84, madeira)
me = bpy.data.meshes.new('lance'); bm = bmesh.new()
pf = [(1.06, .84)]
for i in range(12):
    y0 = 1.06 + i * .29; z = .84 + (i + 1) * E
    pf += [(y0, z - .03), (y0 + .29, z - .03)]
pf += [(4.54, MZB), (1.06 + .30, .84 - .22)]   # face inferior inclinada (laje do lance)
for xx in (P, 1.05):
    pass
vs0 = [bm.verts.new((P, -y, z)) for y, z in pf]; vs1 = [bm.verts.new((1.05, -y, z)) for y, z in pf]
bm.faces.new(vs0[::-1]); bm.faces.new(vs1)
n = len(pf)
for i in range(n): bm.faces.new((vs0[i], vs0[(i + 1) % n], vs1[(i + 1) % n], vs1[i]))
bm.normal_update(); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new('lance', me); bpy.context.collection.objects.link(o); o.data.materials.append(gelo)
for i in range(12):
    y0 = 1.06 + i * .29; z = .84 + (i + 1) * E
    if i < 11: box('piso-lance', P, 1.07, y0 - .02, y0 + .29, z - .03, z, madeira)
# corrimão do lance no lado aberto (x 1,05), como no corte
L0 = mathutils.Vector((1.08, -1.06, .84 + .95)); L1 = mathutils.Vector((1.08, -4.30, .84 + 11 * E + .95))
d = L1 - L0; bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=.022, depth=d.length, location=(L0 + L1) / 2)
c = bpy.context.object; c.rotation_euler = d.to_track_quat('Z', 'Y').to_euler(); c.data.materials.append(grafite)
for yy, zz in ((1.06, .84), (2.5, .84 + 5 * E)):
    box('pilarete', 1.06, 1.10, yy, yy + .04, zz, zz + .95, grafite)
# banheiro (x 0,15-2,70, y 4,00-5,50) com porta P02 para a área de serviço
parede('bwc-n', 'x', 4.00, 4.15, P, 2.70, FL, MZB, gelo)
parede('bwc-l', 'y', 2.55, 2.70, 4.15, D - P, FL, MZB, gelo, [(4.25, 4.98, FL, 2.25)])
box('porta-P02', 2.58, 2.62, 4.25, 4.98, FL, 2.25, marc_b)
# cozinha: bancada na parede leste (cooktop e pia sob a J03), geladeira e área de serviço
box('balcao', 3.80, W - P, P, 2.65, FL, .86, marc_b); box('tampo', 3.78, W - P, P, 2.65, .86, .90, pedra)
for yy in (.62, .80):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=.09, depth=.01, location=(4.10, -yy, .905)); bpy.context.object.data.materials.append(preto)
box('cooktop', 3.90, 4.32, .52, .96, .90, .905, preto)
box('cuba', 3.92, 4.30, 1.55, 2.05, .80, .901, inox); box('torneira', 4.30, 4.34, 1.78, 1.82, .90, 1.20, inox)
box('geladeira', 3.70, W - P, 2.70, 3.58, FL, 2.00, mat('geladeira', (210, 210, 208), .3, .6))
box('tanque-maq', 3.80, W - P, 3.72, D - P, FL, .90, marc_b); box('tampo-serv', 3.78, W - P, 3.72, D - P, .90, .93, pedra)
# estar: sofá voltado para o rack e a TV na parede do banheiro
box('sofa-base', .70, 2.70, 2.10, 2.95, FL, .45, tecido); box('sofa-encosto', .70, 2.70, 2.10, 2.30, .45, .85, tecido)
box('sofa-braco', .70, .85, 2.10, 2.95, .45, .62, tecido); box('sofa-braco', 2.55, 2.70, 2.10, 2.95, .45, .62, tecido)
box('rack', 1.05, 2.70, 3.62, 3.98, FL, .55, madeira)
box('tv', 1.35, 2.45, 3.97, 4.00, 1.05, 1.68, preto)
box('tapete', .90, 2.60, 2.95, 3.55, FL, FL + .01, mat('tapete', (214, 206, 192), .95))
# vegetação externa vista pelos vãos
ceu(32, float(A[5]) if len(A) > 5 else 250, .5)
V = VIEW
if V == 'a':     # do lado da cozinha olhando para a escada, o patamar e o mezanino
    camera(3.62, .42, FL + 1.55, .50, 4.60, 0, 24, .0, 0, 2.5)
elif V == 'b':   # da porta P01, olhando para os fundos: pé-direito duplo, mezanino e J05
    camera(2.80, .32, FL + 1.60, 2.45, 5.50, 0, 24, .21, 0, 2.5)
elif V == 'top':  # conferência: planta vista de cima (sem teto)
    for o in bpy.data.objects:
        if o.name.startswith(('laje-teto', 'forro', 'laje-mez', 'piso-mez', 'gc', 'frente', 'fundos', 'oeste', 'leste')) and o.location.z > 2.4: o.hide_render = True
    bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam; cam.data.type = 'ORTHO'; cam.data.ortho_scale = 6.2
    cam.location = (W / 2, -D / 2, 20); cam.rotation_euler = (0, 0, 0); sc.view_settings.exposure = .5
    sc.render.resolution_x, sc.render.resolution_y = 800, 1000
elif V == 'corte':  # conferência: corte longitudinal olhando para oeste (como o corte BB)
    for o in bpy.data.objects:
        if o.name.startswith('leste') or (o.name.startswith('jan') and o.location.x > 4) or (o.location.x > 3.0 and o.name.startswith(('balcao', 'tampo', 'geladeira', 'tanque', 'cuba', 'torneira', 'cooktop', 'Cylinder'))): o.hide_render = True
    bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam; cam.data.type = 'ORTHO'; cam.data.ortho_scale = 6.6
    cam.location = (20, -D / 2, 3.0); cam.rotation_euler = (math.radians(90), 0, math.radians(90)); sc.view_settings.exposure = .5
    sc.render.resolution_x, sc.render.resolution_y = 1000, 1000
render()
