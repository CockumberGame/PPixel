import bpy
from bpy.types import Operator

try:
    from bpy_extras.io_utils import ImportHelper
except Exception:  # Blender build-specific fallback
    class ImportHelper:  # type: ignore
        pass

from .node_builder import attach_processor, sync_active_material_nodes
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


class PST_OT_SyncPixelProcessor(Operator):
    bl_idname = "pst.sync_pixel_processor"
    bl_label = "Sync Settings To Material"
    bl_description = "Apply current panel settings to Pixel Shader Toolkit nodes in active material"

    def execute(self, context):
        updated = sync_active_material_nodes(context, context.scene.pst_settings)
        self.report({"INFO"}, f"Synced {updated} PST node(s)")
        return {"FINISHED"}


class PST_OT_OpenShadingWorkspace(Operator):
    bl_idname = "pst.open_shading_workspace"
    bl_label = "Open Shading Workspace"
    bl_description = "Switch to Blender Shading workspace where full PST controls are available"

    def execute(self, context):
        workspace = bpy.data.workspaces.get("Shading")
        if not workspace:
            self.report({"WARNING"}, "Shading workspace not found")
            return {"CANCELLED"}

        context.window.workspace = workspace
        self.report({"INFO"}, "Switched to Shading workspace")
        return {"FINISHED"}


class PST_OT_RefreshPaletteList(Operator):
    bl_idname = "pst.refresh_palettes"
    bl_label = "Refresh Palettes"

    def execute(self, context):
        PALETTE_MANAGER.refresh()
        sync_active_material_nodes(context, context.scene.pst_settings)
        self.report({"INFO"}, "Palettes reloaded")
        return {"FINISHED"}


class PST_OT_ImportGPLPalette(Operator, ImportHelper):
    bl_idname = "pst.import_gpl_palette"
    bl_label = "Import GPL Palette"
    filename_ext = ".gpl"

    filter_glob: bpy.props.StringProperty(default="*.gpl", options={"HIDDEN"})

    def execute(self, context):
        try:
            imported = PALETTE_MANAGER.import_gpl(self.filepath)
            sync_active_material_nodes(context, context.scene.pst_settings)
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

    def execute(self, context):
        try:
            imported = PALETTE_MANAGER.import_hex_list(self.filepath)
            sync_active_material_nodes(context, context.scene.pst_settings)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Imported palette: {imported}")
        return {"FINISHED"}
