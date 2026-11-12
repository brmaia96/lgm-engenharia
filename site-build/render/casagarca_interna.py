# Casa Garça, internas: montado SÓ com a Planta Baixa e o Corte A-A / B-B do Projeto Executivo (prancha 01/02 e 02/02).
# Planta: x da face externa oeste da casa (0) para a leste (7,35); y da face externa dos fundos (0) para a frente (12,40); paredes 0,15.
# Pé-direito 2,80 sob laje pré (cortes A-A e B-B). Quadro de esquadrias: PCV250 porta de correr de vidro 2,50 x 2,10 (sala/varanda);
# PCM90 porta de correr de madeira 0,90 x 2,10 (sala/circulação); PAV80 porta de abrir de vidro 0,80 x 2,10 e JCV150 1,50 x 1,00
# peitoril 1,10 (cozinha/lavanderia); JCV150 da suíte na parede oeste; PAM80 da suíte para a circulação.
# Ambientes (planta): lavanderia y 0,15-1,11; cozinha x 4,10-7,20, y 1,26-5,34 (12,66 m²); sala estar/jantar y 5,34-10,76 (16,78 m²);
# suíte x 0,15-3,95, y 0,15-2,95, com o braço de 1,00 x 1,55 do armário até a porta (12,19 m²).
# Layout da planta: bancada com pia sob a JCV150, geladeira na parede leste, bancada de 2,00 com cooktop e banquetas, mesa de jantar,
# sofá na parede leste, painel de TV na parede oeste; suíte com cama de casal, criado-mudo, painel e armário de 1,80.
# Acabamentos do memorial: porcelanato, látex, forro em laje. Cores: neutras (a prancha não define).
import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'int_lib.py')).read())
P = .15; H = 2.80
latex = mat('latex', (238, 236, 231), .9); ruido(latex, 80, (232, 230, 225), (242, 240, 235), .02)
piso = mat('porcelanato', (212, 207, 198), .3); piso_placas(piso, .90, (214, 209, 200), (206, 201, 192))
madeira = mat('madeira', (170, 134, 98), .55); veio(madeira, 3, (154, 118, 84), (182, 146, 108))
porta_m = mat('porta-madeira', (150, 116, 84), .5); veio(porta_m, 3, (138, 104, 74), (160, 126, 92))
marc = mat('marcenaria', (226, 222, 214), .45)
pedra = mat('bancada', (60, 60, 62), .3); ruido(pedra, 40, (52, 52, 54), (70, 70, 72), .01)
inox = mat('inox', (190, 190, 188), .25, 1.)
preto = mat('preto', (24, 24, 26), .3)
tecido = mat('tecido', (184, 176, 164), .9); ruido(tecido, 200, (176, 168, 156), (192, 184, 172), .2)
linho = mat('linho', (228, 222, 212), .9); fronha = mat('fronha', (240, 237, 231), .9)
grama = mat('grama', (98, 122, 76), .95); ruido(grama, 300, (86, 110, 66), (110, 134, 86), .15, 14)
muro = mat('muro', (222, 218, 210), .9)
# piso, laje e paredes externas
box('piso', P, 7.20, P, 12.25, -.02, 0, piso)
box('laje', -.1, 7.45, -.1, 10.91, H, H + .2, latex)
box('ext', -15, 25, -15, 30, -.05, -.04, mat('terreno', (160, 156, 148), .95))
box('jardim-lateral', -2.40, 0, 0, 12.25, -.04, -.02, grama); box('divisa-o', -2.55, -2.40, -2, 20, 0, 2.0, muro)
box('divisa-l', 7.35, 7.50, -2, 20, 0, 2.0, muro); box('fundo-lote', -2.55, 7.5, -1.85, -1.70, 0, 2.0, muro)
box('quintal', -2.40, 7.35, -1.70, 0, -.04, -.02, grama)
parede('fundos', 'x', 0, P, 0, 7.35, 0, H, latex)
parede('oeste', 'y', 0, P, P, 10.91, 0, H, latex, [(1.40, 2.90, 1.10, 2.10)])
parede('leste', 'y', 7.20, 7.35, P, 10.91, 0, H, latex)
janela('y', P / 2, 1.40, 2.90, 1.10, 2.10); portal('y', 0, 1.40, 2.90, 1.10, 2.10, -1)
# parede da frente da sala com a PCV250 (x 4,40-6,90) e varanda coberta / garagem à frente
parede('frente-sala', 'x', 10.76, 10.91, 4.10, 7.20, 0, H, latex, [(4.40, 6.90, 0, 2.10)])
for k, (a, b) in enumerate(((4.40, 5.66), (5.64, 6.90))):
    box('pcv-quadro', a, b, 10.80 + .03 * k, 10.84 + .03 * k, 0, .05, alu_e); box('pcv-quadro', a, b, 10.80 + .03 * k, 10.84 + .03 * k, 2.05, 2.10, alu_e)
    box('pcv-quadro', a, a + .05, 10.80 + .03 * k, 10.84 + .03 * k, 0, 2.10, alu_e); box('pcv-quadro', b - .05, b, 10.80 + .03 * k, 10.84 + .03 * k, 0, 2.10, alu_e)
    box('pcv-vidro', a + .05, b - .05, 10.815 + .03 * k, 10.825 + .03 * k, .05, 2.05, vidro_m)
portal('x', 10.91, 4.40, 6.90, 0, 2.10, 1)
box('varanda-piso', 4.10, 7.20, 10.91, 12.40, -.03, -.01, mat('piso-ext', (196, 192, 184), .8))
box('varanda-cob', 4.10, 7.35, 10.91, 12.40, H, H + .15, latex)
box('garagem-cob', 0, 8.70, 12.40, 17.5, 3.05, 3.15, mat('sanduiche', (200, 200, 198), .5, .3))
box('frente-quartos', P, 4.10, 10.91, 12.35, 0, H, latex)
# parede interna oeste da cozinha e da sala (x 3,95-4,10) com a PCM90 (y 5,35-6,25)
parede('int-oeste', 'y', 3.95, 4.10, P, 10.76, 0, H, latex, [(5.35, 6.25, 0, 2.10)])
box('pcm90', 3.90, 3.94, 5.20, 6.10, 0, 2.10, porta_m)          # folha de correr parcialmente aberta, do lado da circulação
# divisa cozinha / lavanderia (y 1,11-1,26): PAV80 x 4,23-5,03 e JCV150 x 5,05-6,55
parede('div-lav', 'x', 1.11, 1.26, 4.10, 7.20, 0, H, latex, [(4.23, 5.03, 0, 2.10), (5.05, 6.55, 1.10, 2.10)])
janela('x', 1.185, 5.05, 6.55, 1.10, 2.10)
box('pav80-quadro', 4.23, 4.27, 1.15, 1.22, 0, 2.10, alu_e); box('pav80-quadro', 4.99, 5.03, 1.15, 1.22, 0, 2.10, alu_e); box('pav80-quadro', 4.23, 5.03, 1.15, 1.22, 2.06, 2.10, alu_e)
box('pav80-vidro', 4.27, 4.99, 1.18, 1.19, 0, 2.06, vidro_m)
# lavanderia: bancada, tanque e luz indireta (a planta não mostra o vão externo dela; luz escondida, nenhum vão inventado)
box('lav-bancada', 5.9, 7.2, P, .75, 0, .9, marc); box('lav-tampo', 5.9, 7.2, P, .75, .9, .93, mat('lav-pedra', (220, 216, 208), .3))
bpy.ops.object.light_add(type='AREA', location=(5.6, -.55, 2.6)); Ll = bpy.context.object; Ll.data.size = 2.6; Ll.data.size_y = .8; Ll.data.energy = 220
Ll.data.color = (1.0, .97, .92); Ll.visible_camera = False
# suíte: paredes internas
parede('suite-s', 'x', 2.95, 3.10, P, 2.95, 0, H, latex)                 # entre a suíte e o BHO 02
parede('suite-arm-o', 'y', 2.80, 2.95, 2.95, 4.50, 0, H, latex)          # braço do armário até a porta
parede('bho02-s', 'x', 4.50, 4.65, P, 2.95, 0, H, latex)
box('pam80-folha', 2.95, 3.03, 4.50, 5.28, 0, 2.10, porta_m)             # porta da suíte aberta para a circulação
box('pam80-bat', 2.95, 3.95, 4.50, 4.56, 2.10, H, latex)
# ---- cozinha ----
box('bancada-pia', 5.05, 7.20, 1.26, 1.86, 0, .86, marc); box('tampo-pia', 5.05, 7.20, 1.26, 1.88, .86, .90, pedra)
box('cuba', 5.55, 6.10, 1.40, 1.78, .72, .901, inox); box('torneira', 5.80, 5.84, 1.30, 1.34, .90, 1.25, inox); box('bica', 5.80, 5.84, 1.30, 1.50, 1.21, 1.25, inox)
box('geladeira', 6.47, 7.18, 2.28, 3.10, 0, 1.85, mat('geladeira', (205, 205, 203), .3, .6))
box('peninsula', 5.20, 7.20, 3.85, 4.45, 0, .86, marc); box('tampo-pen', 5.18, 7.20, 3.85, 4.55, .86, .90, pedra)
box('cooktop', 5.65, 6.25, 3.95, 4.35, .90, .905, preto)
for k in range(3):
    xx = 5.55 + k * .55
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=.19, depth=.05, location=(xx, -4.78, .70)); bpy.context.object.data.materials.append(madeira)
    for dx, dy in ((-.12, -.12), (.12, -.12), (-.12, .12), (.12, .12)):
        box('banq-pe', xx + dx - .012, xx + dx + .012, 4.78 + dy - .012, 4.78 + dy + .012, 0, .68, preto)
# ---- jantar ----
box('mesa', 5.50, 7.10, 5.75, 6.65, .72, .76, madeira)
for xx in (5.60, 7.00):
    for yy in (5.80, 6.60): box('mesa-pe', xx - .025, xx + .025, yy - .025, yy + .025, 0, .72, preto)
def cadeira(x, y, vira):
    box('cad-assento', x - .22, x + .22, y - .22, y + .22, .44, .48, tecido)
    for dx, dy in ((-.19, -.19), (.19, -.19), (-.19, .19), (.19, .19)): box('cad-pe', x + dx - .012, x + dx + .012, y + dy - .012, y + dy + .012, 0, .44, preto)
    yb = y + .21 * vira; box('cad-enc', x - .22, x + .22, yb - .02, yb + .02, .48, .88, tecido)
for xx in (5.95, 6.65): cadeira(xx, 5.50, -1); cadeira(xx, 6.90, 1)
# ---- estar ----
box('sofa-base', 6.20, 7.16, 7.45, 10.25, 0, .42, tecido); box('sofa-enc', 6.95, 7.16, 7.45, 10.25, .42, .82, tecido)
box('sofa-braco', 6.20, 7.16, 7.45, 7.62, .42, .60, tecido); box('sofa-braco', 6.20, 7.16, 10.08, 10.25, .42, .60, tecido)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1.0, depth=.01, location=(5.40, -8.85, .006)); bpy.context.object.data.materials.append(mat('tapete', (206, 198, 184), .95))
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=.40, depth=.04, location=(5.55, -8.85, .40)); bpy.context.object.data.materials.append(madeira)
box('mesa-centro-pe', 5.53, 5.57, 8.83, 8.87, 0, .38, preto)
box('painel-tv', 4.10, 4.16, 7.60, 10.10, 0, 2.40, madeira); box('rack', 4.16, 4.60, 7.90, 9.80, .25, .55, marc)
box('tv', 4.16, 4.20, 8.25, 9.45, 1.05, 1.73, preto)
box('aparador', 6.34, 7.16, 10.30, 10.72, 0, .75, madeira)
# ---- suíte ----
box('cama-base', .68, 2.28, .19, 2.18, 0, .30, marc); box('colchao', .70, 2.26, .25, 2.16, .30, .55, linho)
box('cabeceira', .50, 2.46, .15, .23, 0, 1.20, madeira)
for xx in (.80, 1.52): box('travesseiro', xx, xx + .62, .30, .70, .55, .68, fronha)
box('manta', .70, 2.26, 1.55, 2.00, .555, .60, tecido)
box('criado', .18, .60, .19, .73, 0, .50, madeira)
box('painel-suite', .49, 2.61, 2.82, 2.95, 0, .45, madeira)
box('armario', 3.20, 3.95, .19, 2.01, 0, 2.40, marc)
for yy in (.19, .80, 1.40, 2.01): box('arm-junta', 3.195, 3.20, yy - .003, yy + .003, .02, 2.38, mat('junta', (150, 146, 140), .6))
box('arm-sobre', 3.20, 3.95, .19, 2.01, 2.40, H, marc)
ceu(30, float(A[5]) if len(A) > 5 else 250, .55)
V = VIEW
if V == 'a':     # da sala, junto à PCV250, olhando para o jantar e a cozinha
    camera(5.00, 10.45, 1.60, 6.00, 1.30, 0, 24, 0.0, 0, 2.2)
elif V == 'b':   # do canto junto ao armário e à entrada, olhando para a cama e a JCV150
    camera(3.58, 2.86, 1.58, .30, 1.00, 0, 24, -.06, 0, 1.4)
elif V == 'top':
    for o in bpy.data.objects:
        if o.location.z > 2.5 or o.name.startswith(('laje', 'varanda-cob', 'garagem')): o.hide_render = True
    bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam; cam.data.type = 'ORTHO'; cam.data.ortho_scale = 13.0
    cam.location = (3.7, -6.2, 20); cam.rotation_euler = (0, 0, 0); sc.view_settings.exposure = .5
    sc.render.resolution_x, sc.render.resolution_y = 560, 1000
render()
