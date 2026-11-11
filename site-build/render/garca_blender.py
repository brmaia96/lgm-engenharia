# Fachada da obra comercial de Garça, modelada só com as medidas da prancha aprovada (Fachada 04) e renderizada no Cycles.
# Vidro 29,25 x 5,00 m em três vãos (montantes grossos a 32% e 62% da largura), montantes a ~1,05 m, travessa a 3,08 m,
# porta dupla central, painel de alumínio composto de 2,00 m, volume da caixa-d'água 2,00 x 1,50 m à esquerda, muros de divisa de 2,20 m.
# Sem logotipo (a prancha só reserva o espaço), sem carros, pessoas ou vizinhos inventados.
import bpy, math, sys
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = args[0] if args else '/tmp/garca.png'
RW, RH, SPP = (int(args[1]), int(args[2]), int(args[3])) if len(args) > 3 else (1600, 900, 64)
CX, CY, FOC = (float(args[4]), float(args[5]), float(args[6])) if len(args) > 6 else (-15.0, 30.0, 40.0)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = RW, RH; sc.render.film_transparent = False
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'; sc.view_settings.exposure = -0.75
sc.cycles.max_bounces = 6; sc.cycles.glossy_bounces = 4; sc.cycles.transmission_bounces = 6

def mat(name, color, rough=.5, metal=0., trans=0., ior=1.45, spec=.5):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal; b.inputs['Transmission Weight'].default_value = trans; b.inputs['IOR'].default_value = ior
    return m
def box(name, sx, sy, sz, x, y, z, m):
    # x: ao longo da fachada; y: profundidade (positivo = para dentro do prédio); z: altura (base em z)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z + sz / 2)); o = bpy.context.object
    o.scale = (sx, sy, sz); o.name = name; o.data.materials.append(m); return o
def lin(c): return tuple(((v / 255) / 12.92) if v / 255 <= .04045 else (((v / 255 + .055) / 1.055) ** 2.4) for v in c)

GW, GH, PH = 29.25, 5.0, 2.0; X0 = -GW / 2; DEP = 24; ZB = .40   # Fachada 04: vidro de +0,40 a +5,40 sobre faixa de base
alu = mat('alu', lin((196, 198, 200)), .28, .85)
alu2 = mat('junta', lin((120, 124, 128)), .4, .8)
caix = mat('caixilho', lin((168, 171, 173)), .3, .8)
branco = mat('reboco', lin((236, 234, 229)), .85)
vidro = mat('vidro', lin((150, 172, 176)), .0, 0., 1., 1.52)
piso = mat('piso', lin((200, 196, 188)), .35)
teto = mat('teto', lin((240, 239, 236)), .9)
muro = mat('muro', lin((226, 222, 214)), .9)
calc = mat('calcada', lin((178, 174, 166)), .9)
guia = mat('guia', lin((160, 156, 150)), .85)
asf = mat('asfalto', lin((52, 53, 55)), .92)
def ruido(m, esc, a, b):
    nt = m.node_tree; bs = nt.nodes['Principled BSDF']; tx = nt.nodes.new('ShaderNodeTexNoise'); tx.inputs['Scale'].default_value = esc; tx.inputs['Detail'].default_value = 12
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (*a, 1); cr.color_ramp.elements[1].color = (*b, 1)
    nt.links.new(tx.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], bs.inputs['Base Color'])
    bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = .15; nt.links.new(tx.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], bs.inputs['Normal'])
ruido(asf, 180, lin((40, 41, 43)), lin((70, 71, 73)))
preto = mat('puxador', lin((30, 30, 30)), .3, .9)

# fachada
box('base', GW + .3, .30, ZB, 0, .05, 0, mat('base', lin((176, 172, 166)), .85))
box('painel', GW + .3, .12, PH, 0, -.06, ZB + GH, alu)   # painel liso (sem modulacao na prancha)
box('rufo', GW + .3, .30, .06, 0, .05, ZB + GH + PH, alu2)
box('caixa', 2.0, 2.4, 1.5, X0 + 1.0, 1.3, ZB + GH + PH, branco)
box('lat-e', .2, DEP, ZB + GH + PH, X0 - .05, DEP / 2, 0, branco); box('lat-d', .2, DEP, ZB + GH + PH, -X0 + .05, DEP / 2, 0, branco)
box('cobertura', GW, DEP, .2, 0, DEP / 2, ZB + GH + PH - .2, branco)
# interior simples (sem objetos): piso, teto, parede do fundo, e luz difusa de teto
box('piso-int', GW, DEP - .4, .02, 0, DEP / 2, ZB, piso); box('teto-int', GW, DEP - .4, .05, 0, DEP / 2, ZB + GH - .03, teto)
box('fundo', GW, .1, GH, 0, DEP - .3, ZB, branco)
bpy.ops.object.light_add(type='AREA', location=(0, 8, ZB + GH - .1)); L = bpy.context.object; L.data.shape = 'RECTANGLE'
L.data.size, L.data.size_y = GW - 2, 12; L.data.energy = 2200; L.data.color = (1, .96, .9); L.rotation_euler = (math.pi, 0, 0)
# vidro e caixilhos
box('vidro', GW, .02, GH, 0, .01, ZB, vidro)
def fr(w, h, x, z): box('caix', w, .09, h, x, 0, ZB + z, caix)
fr(GW, .07, 0, 0); fr(GW, .07, 0, GH - .07); fr(GW, .05, 0, 3.10)
# Fachada 04: tres vaos praticamente iguais, montantes grossos de 0,21 a 33,2% e 67,4%; oito modulos de 1,20 por vao
B1, B2 = X0 + .332 * GW, X0 + .674 * GW
for a, b in ((X0, B1), (B1, B2), (B2, -X0)):
    for i in range(1, 8): fr(.045, GH, a + (b - a) * i / 8, 0)
for xb in (B1, B2): fr(.21, GH, xb, 0)
fr(.07, GH, X0 + .035, 0); fr(.07, GH, -X0 - .035, 0)
# porta dupla de 2,60 (13,41 a 16,01 a partir da esquerda do vidro)
PX = X0 + 14.71
fr(.07, GH, X0 + 13.41, 0); fr(.07, GH, X0 + 16.01, 0)
box('pux1', .03, .05, 1.2, PX - .12, -.07, ZB + .9, preto); box('pux2', .03, .05, 1.2, PX + .12, -.07, ZB + .9, preto)
# muros de divisa, calçada, guia, rua
# muros de divisa ficam no lote, atras do alinhamento (nao sobre a calcada)
box('muro-e', .15, DEP, 2.2, X0 - .6, DEP / 2, 0, muro); box('muro-d', .15, DEP, 2.2, -X0 + .6, DEP / 2, 0, muro)
box('calcada', 90, 6, .15, 0, -3, -.15, calc)
ruido(calc, 60, lin((168, 164, 156)), lin((190, 186, 178)))
xj = -44.0
while xj < 45: box('junta-c', .015, 6, .002, xj, -3, 0, guia); xj += 1.5; box('guia', 90, .15, .16, 0, -6.05, -.16, guia)
box('rua', 90, 40, .02, 0, -26, -.32, asf)

# céu físico (Nishita), sol de manhã vindo da esquerda e da frente
w = bpy.data.worlds.new('ceu'); sc.world = w; w.use_nodes = True; nt = w.node_tree
sky = nt.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'NISHITA'; sky.sun_elevation = math.radians(32); sky.sun_rotation = math.radians(230)
sky.air_density = 1.0; sky.dust_density = 1.2; sky.sun_intensity = .5
bg = nt.nodes['Background']; bg.inputs['Strength'].default_value = .32
nt.links.new(sky.outputs['Color'], bg.inputs['Color'])
# câmera na altura do olho, do outro lado da rua, em leve três quartos
bpy.ops.object.camera_add(location=(CX, -CY, 1.65)); cam = bpy.context.object; sc.camera = cam
cam.data.lens = FOC; cam.data.sensor_width = 36
import mathutils
d = mathutils.Vector((0.0, 0, 3.6)) - cam.location; cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
cam.data.shift_y = .07
sc.render.filepath = OUT; bpy.ops.render.render(write_still=True); print('ok', OUT)
