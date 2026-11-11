# Casa em Garça: modelo montado com as cotas das pranchas executivas (Fachada Norte, Detalhe da Fachada, Planta de Cobertura, Corte A-A)
# e renderizado no Cycles. Eixos: x ao longo da rua (0 a 10 m), y da rua para o fundo, z altura.
# Fachada: muro frontal até 2,80 com portão basculante 5,00 x 2,40 (x 2,00-7,00), pilar 0,40, portão social 1,20 x 2,40 (x 7,40-8,60);
# tabeira metálica 8,70 x 0,50 (z 2,80-3,30) sobre a garagem coberta de 5,00 m; volumes da casa com platibanda até 4,50
# (x 1,90-6,54 e 6,54-10,00); caixa-d'água 2,95 m até 5,30; muros de divisa de 2,00. Cores: as pranchas não definem; neutras
# (reboco branco, tabeira e portões em grafite).
import bpy, math, sys, mathutils
A = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = A[0] if A else '/tmp/cg.png'
RW, RH, SPP = (int(A[1]), int(A[2]), int(A[3])) if len(A) > 3 else (1200, 800, 32)
VIEW = A[4] if len(A) > 4 else 'persp'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = RW, RH
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; sc.view_settings.exposure = -0.6
def lin(c): return tuple(((v / 255) / 12.92) if v / 255 <= .04045 else (((v / 255 + .055) / 1.055) ** 2.4) for v in c)
def mat(n, c, r=.5, m=0.):
    M = bpy.data.materials.new(n); M.use_nodes = True; b = M.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*lin(c), 1); b.inputs['Roughness'].default_value = r; b.inputs['Metallic'].default_value = m; return M
def ruido(M, esc, a, b, bump=.1, det=10):
    nt = M.node_tree; bs = nt.nodes['Principled BSDF']; tx = nt.nodes.new('ShaderNodeTexNoise'); tx.inputs['Scale'].default_value = esc; tx.inputs['Detail'].default_value = det
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (*lin(a), 1); cr.color_ramp.elements[1].color = (*lin(b), 1)
    nt.links.new(tx.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], bs.inputs['Base Color'])
    bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = bump; nt.links.new(tx.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], bs.inputs['Normal'])
reboco = mat('reboco', (238, 236, 231), .85); ruido(reboco, 90, (230, 228, 223), (243, 241, 237), .05)
grafite = mat('grafite', (52, 54, 57), .4, .7)
lamina = mat('lamina', (66, 68, 72), .35, .75)
muro = mat('muro', (222, 218, 210), .9); ruido(muro, 70, (210, 206, 198), (228, 224, 216), .06)
calc = mat('calcada', (176, 172, 164), .9); ruido(calc, 60, (166, 162, 154), (188, 184, 176), .1)
guia = mat('guia', (158, 154, 148), .85)
asf = mat('asfalto', (52, 53, 55), .92); ruido(asf, 180, (40, 41, 43), (70, 71, 73), .15, 12)
piso = mat('piso-garagem', (150, 148, 144), .7)
def box(n, x0, x1, y0, y1, z0, z1, M):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)); o = bpy.context.object
    o.scale = (x1 - x0, y1 - y0, z1 - z0); o.name = n; o.data.materials.append(M); return o
# muro frontal (y 0-0,15) com os vãos dos portões
box('muro-f-esq', 0, 2.00, 0, .15, 0, 2.80, reboco)
box('pilar', 7.00, 7.40, 0, .15, 0, 2.80, reboco)
box('muro-f-dir', 8.60, 10.0, 0, .15, 0, 2.80, reboco)
box('verga-1', 2.00, 7.00, 0, .15, 2.40, 2.80, reboco); box('verga-2', 7.40, 8.60, 0, .15, 2.40, 2.80, reboco)
# portões em lâminas horizontais de alumínio (basculante 5,00 x 2,40 e social 1,20 x 2,40)
for x0, x1 in ((2.00, 7.00), (7.40, 8.60)):
    box('quadro', x0, x1, .04, .10, 0, 2.40, grafite)
    z = .08
    while z < 2.34: box('lamina', x0 + .04, x1 - .04, .02, .12, z, z + .07, lamina); z += .12
box('puxador', 8.45, 8.48, -.02, .02, 1.0, 1.3, grafite)
# tabeira metálica da garagem (8,70 x 0,50) e cobertura de telha sanduíche
box('tabeira', 0, 8.70, -.05, .10, 2.80, 3.30, grafite)
box('cob-garagem', 0, 8.70, .10, 5.15, 3.05, 3.15, mat('sanduiche', (190, 192, 194), .45, .6))
box('piso-gar', .15, 8.70, .15, 5.15, -.01, .01, piso)
# casa: volumes com platibanda (fachada norte: 1,90 | 4,64 | 3,46), recuo de 5,15 da rua
# Fachadas Leste/Oeste: platibanda frontal de 0,15 ate 4,50; corpo da casa a 4,00 ate o fundo (5,00 + 12,25 = 17,25)
box('plat-central', 1.90, 6.54, 5.15, 5.30, 0, 4.50, reboco)
box('plat-direita', 6.54, 9.85, 5.15, 5.30, 0, 4.50, reboco)
box('volume-central', 1.90, 6.54, 5.15, 17.25, 0, 4.00, reboco)
box('volume-direito', 6.54, 9.85, 5.15, 17.25, 0, 4.00, reboco)
box('moldura-recuo', 6.70, 9.70, 5.10, 5.16, 3.30, 4.30, mat('rebaixo', (226, 224, 219), .85))   # requadro da fachada do volume direito
box('caixa-dagua', 2.61, 5.56, 11.05, 14.30, 4.00, 5.30, reboco)
box('pingadeira', 1.88, 9.87, 5.12, 5.33, 4.50, 4.53, mat('rufo', (205, 205, 203), .4, .5))
box('pingadeira2', 1.88, 9.87, 5.30, 17.27, 4.00, 4.03, mat('rufo2', (205, 205, 203), .4, .5))
# muros de divisa (2,00) e lote
box('divisa-e', 0, .15, .15, 20, 0, 2.00, muro); box('divisa-d', 9.85, 10.0, .15, 20, 0, 2.00, muro)
box('calcada', -30, 40, -2.5, 0, -.15, 0, calc); box('guia', -30, 40, -2.65, -2.5, -.16, 0, guia)
box('rua', -30, 40, -14, -2.65, -.32, -.30, asf)
# vizinhos: só os muros de divisa, sem casas inventadas
box('chao', -30, 40, 0, 30, -.06, -.05, mat('terreno', (150, 146, 136), .95))
# céu físico e câmera
w = bpy.data.worlds.new('ceu'); sc.world = w; w.use_nodes = True; nw = w.node_tree
sky = nw.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'NISHITA'; sky.sun_elevation = math.radians(36); sky.sun_rotation = math.radians(215)
sky.sun_intensity = .5; nw.nodes['Background'].inputs['Strength'].default_value = .3; nw.links.new(sky.outputs['Color'], nw.nodes['Background'].inputs['Color'])
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
if VIEW == 'ortho':
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = 11.5; cam.location = (5, -30, 2.7); cam.rotation_euler = (math.radians(90), 0, 0)
else:
    cx, cy, f = (float(A[5]), float(A[6]), float(A[7])) if len(A) > 7 else (-3.5, -11.0, 30.0)
    cam.location = (cx, cy, 1.65); cam.data.lens = f; cam.data.sensor_width = 36
    tg = mathutils.Vector((float(A[8]) if len(A) > 8 else 5.2, 2.0, 2.6)); cam.rotation_euler = (tg - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.data.shift_y = -.02
sc.render.filepath = OUT; bpy.ops.render.render(write_still=True); print('ok', OUT)
