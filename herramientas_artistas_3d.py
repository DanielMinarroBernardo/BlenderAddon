bl_info = {
    "name": "Herramientas Artistas 3D",
    "author": "Daniel Miñarro Bernardo",
    "version": (1, 0, 0),
    "blender": (4, 2, 3),
    "location": "View3D > Herramientas",
    "description": "Un conjunto de herramientas para crear mallas básicas, aplicar físicas y manipular objetos",
    "category": "3D View",
}

import bpy
from bpy.types import Menu, Operator, Panel, PropertyGroup

# Propiedades para ajustar parámetros de las mallas
class MYTOOLS_Properties(bpy.types.PropertyGroup):
    size: bpy.props.FloatProperty(name="Tamaño", default=2.0, min=0.1, max=10.0, description="Tamaño de la figura")
    segments: bpy.props.IntProperty(name="Segmentos", default=32, min=3, max=128, description="Número de segmentos (para esferas y cilindros)")
    rings: bpy.props.IntProperty(name="Anillos", default=16, min=3, max=64, description="Número de anillos (para la esfera UV)")
    depth: bpy.props.FloatProperty(name="Altura", default=2.0, min=0.1, max=10.0, description="Altura (para cilindros y conos)")

# Panel principal
class MYTOOLS_PT_MainPanel(Panel):
    bl_label = "Mi Panel de Herramientas"
    bl_idname = "VIEW3D_PT_my_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Herramientas"

    def draw(self, context):z
        layout = self.layout
        layout.label(text="Panel principal con dos subpaneles")

# Primer subpanel: Mallas básicas
class MYTOOLS_PT_SubPanel1(Panel):
    bl_label = "Sección 1: Mallas Básicas"
    bl_idname = "VIEW3D_PT_my_subpanel1"
    bl_parent_id = "VIEW3D_PT_my_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Herramientas"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if not hasattr(scene, "mytools_props"):
            layout.label(text="Propiedades no disponibles. Recarga el script.")
            return

        props = scene.mytools_props

        layout.label(text="Ajustar parámetros:")
        layout.prop(props, "size")
        layout.prop(props, "segments")
        layout.prop(props, "rings")
        layout.prop(props, "depth")

        layout.separator()
        layout.label(text="Añadir mallas básicas:")
        layout.operator("mesh.add_cube", text="Añadir Cubo", icon='MESH_CUBE')
        layout.operator("mesh.add_uv_sphere", text="Añadir Esfera UV", icon='MESH_UVSPHERE')
        layout.operator("mesh.add_plane", text="Añadir Plano", icon='MESH_PLANE')
        layout.operator("mesh.add_cylinder", text="Añadir Cilindro", icon='MESH_CYLINDER')
        layout.operator("mesh.add_cone", text="Añadir Cono", icon='MESH_CONE')
        layout.operator("mesh.add_monkey", text="Añadir Mono", icon='MESH_MONKEY')

# Operadores personalizados para las mallas
class MYTOOLS_OT_AddCube(Operator):
    bl_idname = "mesh.add_cube"
    bl_label = "Añadir Cubo"
    bl_description = "Añade un cubo con el tamaño especificado"

    def execute(self, context):
        props = context.scene.mytools_props
        bpy.ops.mesh.primitive_cube_add(size=props.size)
        return {'FINISHED'}

class MYTOOLS_OT_AddUVSphere(Operator):
    bl_idname = "mesh.add_uv_sphere"
    bl_label = "Añadir Esfera UV"
    bl_description = "Añade una esfera UV con los parámetros especificados"

    def execute(self, context):
        props = context.scene.mytools_props
        bpy.ops.mesh.primitive_uv_sphere_add(segments=props.segments, ring_count=props.rings, radius=props.size)
        return {'FINISHED'}

class MYTOOLS_OT_AddPlane(Operator):
    bl_idname = "mesh.add_plane"
    bl_label = "Añadir Plano"
    bl_description = "Añade un plano con el tamaño especificado"

    def execute(self, context):
        props = context.scene.mytools_props
        bpy.ops.mesh.primitive_plane_add(size=props.size)
        return {'FINISHED'}

class MYTOOLS_OT_AddCylinder(Operator):
    bl_idname = "mesh.add_cylinder"
    bl_label = "Añadir Cilindro"
    bl_description = "Añade un cilindro con los parámetros especificados"

    def execute(self, context):
        props = context.scene.mytools_props
        bpy.ops.mesh.primitive_cylinder_add(vertices=props.segments, depth=props.depth, radius=props.size)
        return {'FINISHED'}

class MYTOOLS_OT_AddCone(Operator):
    bl_idname = "mesh.add_cone"
    bl_label = "Añadir Cono"
    bl_description = "Añade un cono con los parámetros especificados"

    def execute(self, context):
        props = context.scene.mytools_props
        bpy.ops.mesh.primitive_cone_add(vertices=props.segments, depth=props.depth, radius1=props.size)
        return {'FINISHED'}

class MYTOOLS_OT_AddMonkey(Operator):
    bl_idname = "mesh.add_monkey"
    bl_label = "Añadir Monkey"
    bl_description = "Añade un mono con los parámetros especificados"

    def execute(self, context):
        props = context.scene.mytools_props
        bpy.ops.mesh.primitive_monkey_add(size=props.size)
        return {'FINISHED'}

# Operador para mover el origen del objeto al origen del mundo
class MoveOriginToWorldOriginOperator(Operator):
    """Mover el origen del objeto al origen del mundo (0, 0, 0)"""
    bl_idname = "object.move_origin_to_world"
    bl_label = "Mover Origen al Origen del Mundo"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object

        if obj is None:
            self.report({'WARNING'}, "No hay ningún objeto seleccionado")
            return {'CANCELLED'}

        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
        obj.location = (0, 0, 0)

        self.report({'INFO'}, f"El origen del objeto {obj.name} se ha movido al origen del mundo")
        return {'FINISHED'}

# Operador para crear un plano con físicas
class CreatePlaneWithPhysicsOperator(Operator):
    """Crear un plano con subdivisión y físicas de tela"""
    bl_idname = "object.create_plane_with_physics"
    bl_label = "Crear Cojín"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        obj = bpy.context.object
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.subdivide(number_cuts=40)
        bpy.ops.mesh.extrude_region_move(
            MESH_OT_extrude_region={"use_normal_flip": False},
            TRANSFORM_OT_translate={"value": (0, 0, 0.1), "orient_type": 'NORMAL'}
        )
        bpy.ops.mesh.loopcut_slide(
            MESH_OT_loopcut={"number_cuts": 1},
            TRANSFORM_OT_edge_slide={"value": 0}
        )
        bpy.ops.transform.resize(value=(1.03, 1.03, 1.03))
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.modifier_add(type='CLOTH')
        cloth_modifier = obj.modifiers["Cloth"]
        cloth_modifier.settings.use_pressure = True
        cloth_modifier.settings.uniform_pressure_force = 3
        cloth_modifier.settings.effector_weights.gravity = 0
        self.report({'INFO'}, "Plano con físicas creado exitosamente")
        return {'FINISHED'}

# Operador para crear un cubo con configuraciones de fluido
class CreateFluidCubeOperator(Operator):
    """Crear un cubo con configuración de dominio líquido"""
    bl_idname = "object.create_fluid_cube"
    bl_label = "Crear Cubo de Fluido"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.object.modifier_add(type='FLUID')
        bpy.ops.object.shade_smooth()
        bpy.ops.object.material_slot_add()
        bpy.ops.object.quick_liquid()
        obj = bpy.context.object
        fluid_modifier = obj.modifiers["Fluid"]
        fluid_modifier.fluid_type = 'DOMAIN'
        fluid_modifier.domain_settings.domain_type = 'LIQUID'
        self.report({'INFO'}, "Cubo de fluido creado exitosamente")
        return {'FINISHED'}

# Menú radial
class OBJECT_MT_RadialMenu(Menu):
    bl_label = "Herramientas Artistas 3D"
    bl_idname = "OBJECT_MT_radial_menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator(MoveOriginToWorldOriginOperator.bl_idname, text="Mover Origen al Origen del Mundo")
        pie.operator(CreatePlaneWithPhysicsOperator.bl_idname, text="Crear Cojín")
        pie.operator(CreateFluidCubeOperator.bl_idname, text="Crear Cubo de Fluido")

# Registro de las clases y operadores
addon_keymaps = []

def register():
    bpy.utils.register_class(MYTOOLS_Properties)
    bpy.utils.register_class(MYTOOLS_PT_MainPanel)
    bpy.utils.register_class(MYTOOLS_PT_SubPanel1)
    bpy.utils.register_class(MYTOOLS_OT_AddCube)
    bpy.utils.register_class(MYTOOLS_OT_AddUVSphere)
    bpy.utils.register_class(MYTOOLS_OT_AddPlane)
    bpy.utils.register_class(MYTOOLS_OT_AddCylinder)
    bpy.utils.register_class(MYTOOLS_OT_AddCone)
    bpy.utils.register_class(MYTOOLS_OT_AddMonkey)
    bpy.utils.register_class(MoveOriginToWorldOriginOperator)
    bpy.utils.register_class(CreatePlaneWithPhysicsOperator)
    bpy.utils.register_class(CreateFluidCubeOperator)
    bpy.utils.register_class(OBJECT_MT_RadialMenu)

    bpy.types.Scene.mytools_props = bpy.props.PointerProperty(type=MYTOOLS_Properties)

    # Asignar un atajo de teclado para el menú radial
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="Object Mode", space_type="EMPTY")
    kmi = km.keymap_items.new("wm.call_menu_pie", 'RIGHTMOUSE', 'PRESS', ctrl=True, alt=True)
    kmi.properties.name = OBJECT_MT_RadialMenu.bl_idname
    addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    del bpy.types.Scene.mytools_props
    bpy.utils.unregister_class(MYTOOLS_Properties)
    bpy.utils.unregister_class(MYTOOLS_PT_MainPanel)
    bpy.utils.unregister_class(MYTOOLS_PT_SubPanel1)
    bpy.utils.unregister_class(MYTOOLS_OT_AddCube)
    bpy.utils.unregister_class(MYTOOLS_OT_AddUVSphere)
    bpy.utils.unregister_class(MYTOOLS_OT_AddPlane)
    bpy.utils.unregister_class(MYTOOLS_OT_AddCylinder)
    bpy.utils.unregister_class(MYTOOLS_OT_AddCone)
    bpy.utils.unregister_class(MYTOOLS_OT_AddMonkey)
    bpy.utils.unregister_class(MoveOriginToWorldOriginOperator)
    bpy.utils.unregister_class(CreatePlaneWithPhysicsOperator)
    bpy.utils.unregister_class(CreateFluidCubeOperator)
    bpy.utils.unregister_class(OBJECT_MT_RadialMenu)

if __name__ == "__main__":
    register()
