from bpy.types import Panel


class PST_PT_View3DQuickPanel(Panel):
    bl_label = "Pixel Shader Toolkit"
    bl_idname = "PST_PT_view3d_quick_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Pixel Toolkit"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.pst_settings

        info = layout.box()
        info.label(text="You are in 3D View N-panel.")
        info.label(text="Full controls live in Shader Editor > N > Pixel Toolkit.")

        row = layout.row(align=True)
        row.operator("pst.open_shading_workspace", icon="SHADING_TEXTURE")
        row.operator("pst.add_pixel_processor", icon="NODETREE")

        quick = layout.box()
        quick.label(text="Quick controls")
        quick.prop(settings, "pixel_size")
        quick.prop(settings, "palette_impact")
        quick.prop(settings, "dither_strength")
        quick.operator("pst.sync_pixel_processor", icon="FILE_REFRESH")
