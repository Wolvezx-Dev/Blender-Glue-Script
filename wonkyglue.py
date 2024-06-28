import bpy
import bmesh

class WolvezxToolsOperator(bpy.types.Operator):
    bl_idname = "mesh.wolvezx_tools_operator"
    bl_label = "Create Glue"
    bl_options = {'REGISTER', 'UNDO'}

    scale_factor: bpy.props.FloatProperty(name="Scale Factor", default=1.8, min=0.1, max=10.0)
    extrude_height: bpy.props.FloatProperty(name="Extrude Height", default=0.82, min=-10.0, max=10.0)

    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)

        # Identify the lowest Z vertices
        min_z = min(v.co.z for v in bm.verts)
        bottom_verts = [v for v in bm.verts if abs(v.co.z - min_z) < 0.001]  # Get vertices close to the min_z

        # Deselect all first
        for v in bm.verts:
            v.select = False

        # Select the vertices that are on the bottom face
        for v in bottom_verts:
            v.select = True

        # Update the mesh
        bmesh.update_edit_mesh(obj.data)
        bpy.ops.mesh.loop_multi_select(ring=False)

        # Duplicate and extrude
        bpy.ops.mesh.duplicate_move()
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value": (0, 0, self.extrude_height)}
        )

        # Another extrusion with no movement, then scale
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value": (0, 0, 0)}
        )
        bpy.ops.transform.resize(
            value=(self.scale_factor, self.scale_factor, self.scale_factor)
        )

        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}

class WolvezxToolsPanel(bpy.types.Panel):
    bl_label = "Wolvezx Tools"
    bl_idname = "OBJECT_PT_wolvezx_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Wolvezx Tools'

    def draw(self, context):
        layout = self.layout
        layout.operator(WolvezxToolsOperator.bl_idname)

def register():
    bpy.utils.register_class(WolvezxToolsOperator)
    bpy.utils.register_class(WolvezxToolsPanel)

def unregister():
    bpy.utils.unregister_class(WolvezxToolsOperator)
    bpy.utils.unregister_class(WolvezxToolsPanel)

if __name__ == "__main__":
    register()
