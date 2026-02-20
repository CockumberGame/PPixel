from bpy.types import Panel

from ..core.node_builder import iter_pst_nodes
from .theme import DEFAULT_THEME, SECTION_ICONS


class PST_PT_MainPanel(Panel):
    bl_label = "Pixel Shader Toolkit"
    bl_idname = "PST_PT_main_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Pixel Toolkit"

    @classmethod
    def poll(cls, context):
        return context.space_data and context.space_data.tree_type == "ShaderNodeTree"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.pst_settings

        obj = context.object
        mat = obj.active_material if obj else None
        node_count = len(iter_pst_nodes(mat)) if mat else 0

        hero = layout.box()
        hero.scale_y = DEFAULT_THEME["section_scale_y"]
        hero.label(text="Pixel Shader Toolkit • Production Panel", icon=SECTION_ICONS["main"])
        hero.label(text="N-panel here = full control. 3D View tab = quick access.")
        hero.label(text=f"Active material PST nodes: {node_count}")

        row = layout.row(align=True)
        row.scale_y = 1.1
        row.operator("pst.add_pixel_processor", icon="NODETREE")
        row.operator("pst.sync_pixel_processor", icon="FILE_REFRESH")

        color_box = layout.box()
        color_box.label(text="Pixel + Color Processing", icon=SECTION_ICONS["color"])
        col = color_box.column(align=True)
        col.scale_y = DEFAULT_THEME["slider_scale_y"]
        col.prop(settings, "pixel_size")
        col.prop(settings, "palette_name")
        col.prop(settings, "palette_impact")
        col.prop(settings, "dither_enabled")
        col.prop(settings, "dither_strength")

        adjust_box = layout.box()
        adjust_box.label(text="Image Adjustments", icon="IMAGE_RGB")
        adjust_box.prop(settings, "brightness")
        adjust_box.prop(settings, "exposure")
        adjust_box.prop(settings, "contrast")
        adjust_box.prop(settings, "saturation")
        adjust_box.prop(settings, "blur")

        tint_row = adjust_box.row(align=True)
        tint_row.prop(settings, "tint_r")
        tint_row.prop(settings, "tint_g")
        tint_row.prop(settings, "tint_b")

        palette_box = layout.box()
        palette_box.label(text="Palette Library", icon=SECTION_ICONS["palette"])
        row = palette_box.row(align=True)
        row.operator("pst.import_gpl_palette", icon="FILE_FOLDER")
        row.operator("pst.import_hex_palette", icon="IMPORT")
        palette_box.operator("pst.refresh_palettes", icon="FILE_REFRESH")

        bake_box = layout.box()
        bake_box.label(text="Bake Output", icon=SECTION_ICONS["bake"])
        bake_box.prop(settings, "bake_resolution")
        bake_box.prop(settings, "bake_image_name")
        bake_box.operator("pst.bake_to_new_texture", icon="RENDER_STILL")
