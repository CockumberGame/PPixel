import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from .node_builder import attach_processor
from ..palette.manager import PALETTE_MANAGER


class PST_OT_AddPixelProcessor(Operator):
    bl_idname = "pst.add_pixel_processor"
    bl_label = "Add Pixel Processor"
    bl_description = "Insert Pixel Shader Toolkit node group between texture source and Principled BSDF"

    def execute(self, context):
        settings = context.scene.pst_settings
        obj = context.object
        if not obj or not obj.active_material:
            self.report({"ERROR"}, "Select an object with an active material")
            return {"CANCELLED"}

        try:
            attach_processor(obj.active_material, settings)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        self.report({"INFO"}, "Pixel processor added")
        return {"FINISHED"}


class PST_OT_RefreshPaletteList(Operator):
    bl_idname = "pst.refresh_palettes"
    bl_label = "Refresh Palettes"

    def execute(self, _context):
        PALETTE_MANAGER.refresh()
        self.report({"INFO"}, "Palettes reloaded")
        return {"FINISHED"}


class PST_OT_ImportGPLPalette(Operator, ImportHelper):
    bl_idname = "pst.import_gpl_palette"
    bl_label = "Import GPL Palette"
    filename_ext = ".gpl"

    filter_glob: bpy.props.StringProperty(default="*.gpl", options={"HIDDEN"})

    def execute(self, _context):
        try:
            imported = PALETTE_MANAGER.import_gpl(self.filepath)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Imported palette: {imported}")
        return {"FINISHED"}


class PST_OT_ImportHexPalette(Operator, ImportHelper):
    bl_idname = "pst.import_hex_palette"
    bl_label = "Import HEX Palette"
    filename_ext = ".txt"

    filter_glob: bpy.props.StringProperty(default="*.txt", options={"HIDDEN"})

    def execute(self, _context):
        try:
            imported = PALETTE_MANAGER.import_hex_list(self.filepath)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Imported palette: {imported}")
        return {"FINISHED"}
