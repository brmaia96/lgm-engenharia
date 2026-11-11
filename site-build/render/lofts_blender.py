# Três lofts em steel frame (Angra dos Reis): modelo montado com as medidas das vistas do próprio modelo Revit
# (implantação vista de cima, elevação de acesso dos três lofts, elevação frontal do loft) e das cotas do projeto em LSF
# (largura 89 + 4300 + 89 mm, altura 6,00 m). Lote 12 x 30 m (360 m²). Eixos: X do fundo (0) para a rua (30),
# Y da divisa norte (0) para a sul (12), z altura. Fachadas dos lofts voltadas para o corredor de acesso (Y = 4,73).
# Vegetação do paisagismo (palmeiras e agaves) fora: não foi modelada, para não inventar espécie nem porte.
import bpy, math, sys, mathutils
A = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = A[0] if A else '/tmp/lofts.png'
RW, RH, SPP = (int(A[1]), int(A[2]), int(A[3])) if len(A) > 3 else (1200, 800, 32)
VIEW = A[4] if len(A) > 4 else 'persp'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = RW, RH
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; sc.view_settings.exposure = -0.7
def lin(c): return tuple(((v / 255) / 12.92) if v / 255 <= .04045 else (((v / 255 + .055) / 1.055) ** 2.4) for v in c)
def mat(n, c, r=.5, m=0.):
    M = bpy.data.materials.new(n); M.use_nodes = True; b = M.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*lin(c), 1); b.inputs['Roughness'].default_value = r; b.inputs['Metallic'].default_value = m; return M
def ruido(M, esc, a, b, bump=.1, det=10):
    nt = M.node_tree; bs = nt.nodes['Principled BSDF']; tx = nt.nodes.new('ShaderNodeTexNoise'); tx.inputs['Scale'].default_value = esc; tx.inputs['Detail'].default_value = det
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (*lin(a), 1); cr.color_ramp.elements[1].color = (*lin(b), 1)
    nt.links.new(tx.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], bs.inputs['Base Color'])
    bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = bump; nt.links.new(tx.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], bs.inputs['Normal'])
reboco = mat('reboco', (240, 238, 233), .85); ruido(reboco, 90, (232, 230, 225), (245, 243, 239), .05)
junta = mat('junta', (200, 198, 194), .9)
porta = mat('porta', (74, 76, 79), .45, .5)
inox = mat('inox', (200, 200, 198), .25, 1.)
caix = mat('caixilho', (60, 60, 62), .4, .6)
vidro = mat('vidro', (40, 46, 50), .05, .3)
pav = mat('pavimento', (112, 112, 110), .9); ruido(pav, 18, (104, 104, 102), (120, 120, 117), .05)
calc = mat('calcada', (214, 211, 204), .85); ruido(calc, 60, (204, 201, 194), (222, 219, 212), .08)
grama = mat('grama', (92, 120, 70), .95); ruido(grama, 300, (80, 104, 62), (104, 128, 80), .15, 14)
muro = mat('muro', (232, 229, 222), .9); ruido(muro, 70, (222, 219, 212), (238, 235, 228), .06)
def box(n, x0, x1, y0, y1, z0, z1, M):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)); o = bpy.context.object
    o.scale = (x1 - x0, y1 - y0, z1 - z0); o.name = n; o.data.materials.append(M); return o
W, YF, YB, H = 4.478, 4.73, 10.63, 6.00
for k, x0 in enumerate((3.48, 11.07, 18.63)):
    x1 = x0 + W
    box('base', x0 - .62, x1 + .62, YF - .62, YB + .62, -.02, .05, calc)          # calçada em volta
    box('loft', x0, x1, YF, YB, 0, H, reboco)
    box('rufo', x0 - .04, x1 + .04, YF - .04, YB + .04, H, H + .04, mat('rufo%d' % k, (214, 213, 210), .4, .4))
    box('junta-f', x0, x1, YF - .005, YF + .01, 3.06, 3.08, junta)               # junta horizontal da fachada (elevação frontal)
    box('porta', x0 + 2.08, x0 + 3.31, YF - .03, YF + .02, .05, 2.30, porta)
    box('batente', x0 + 2.04, x0 + 3.35, YF - .02, YF + .01, .05, 2.34, caix)
    box('puxador', x0 + 3.12, x0 + 3.15, YF - .09, YF - .05, .55, 1.85, inox)
    box('marquise', x0 + 1.90, x1 + 1.02, YF - .65, YF, 2.95, 3.07, reboco)        # implantação: 3,6 x 0,65 m, passa da lateral
    box('janela-lat', x1 - .01, x1 + .03, YF + .20, YF + .90, 2.30, 2.78, caix)
    box('vidro-lat', x1 + .02, x1 + .035, YF + .25, YF + .85, 2.35, 2.73, vidro)
for xa, xb in ((8.58, 10.45), (16.17, 18.01)):
    box('divisoria', xa, xb, YB + .45, YB + .60, 0, 2.20, muro)
# lote: corredor de acesso pavimentado, faixa de jardim, gramado entre os lofts, muros de divisa de 2,20 m
box('gramado', .2, 24.6, .2, 11.8, -.03, .0, grama)
box('corredor', 2.86, 24.6, .27, 3.04, -.02, .015, pav)
box('divisa-n', 0, 24.6, 0, .2, 0, 2.20, muro); box('divisa-s', 0, 24.6, 11.8, 12, 0, 2.20, muro)
box('fundo', 0, .2, 0, 12, 0, 2.20, muro); box('reservatorio', .2, 2.5, 8.9, 11.8, 0, 2.20, muro)
box('muro-rua', 24.6, 24.8, 0, 12, 0, 2.20, muro)
box('chao', -40, 60, -40, 60, -.06, -.05, mat('terreno', (150, 146, 136), .95))
w = bpy.data.worlds.new('ceu'); sc.world = w; w.use_nodes = True; nw = w.node_tree
sky = nw.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'NISHITA'; sky.sun_elevation = math.radians(38); sky.sun_rotation = math.radians(float(A[9]) if len(A) > 9 else 150)
sky.sun_intensity = .5; nw.nodes['Background'].inputs['Strength'].default_value = .3; nw.links.new(sky.outputs['Color'], nw.nodes['Background'].inputs['Color'])
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
if VIEW == 'ortho':   # vista de conferência: elevação de acesso, olhando para +Y
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = 31; cam.location = (12.4, -20, 3.0); cam.rotation_euler = (math.radians(90), 0, 0)
    bpy.data.objects['divisa-n'].hide_render = True
else:
    cx, cy, f = (float(A[5]), float(A[6]), float(A[7])) if len(A) > 7 else (24.0, .7, 22.0)
    cam.location = (cx, cy, 1.60); cam.data.lens = f; cam.data.sensor_width = 36
    tg = mathutils.Vector((float(A[8]) if len(A) > 8 else 15.0, 5.5, 1.60)); cam.rotation_euler = (tg - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.data.shift_y = .13
sc.render.filepath = OUT; bpy.ops.render.render(write_still=True); print('ok', OUT)
