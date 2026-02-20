bl_info = {
    "name": "Pixel Shader Toolkit",
    "author": "PPixel",
    "version": (0, 2, 0),
    "blender": (3, 6, 0),
    "location": "3D View (N) & Shader Editor (N) > Pixel Toolkit",
    "description": "Procedural pixel/palette/dither shader processor for materials",
    "category": "Material",
}

import bpy

from .core.properties import PSTProperties
from .core.pipeline import (
    PST_OT_AddPixelProcessor,
    PST_OT_ImportGPLPalette,
    PST_OT_ImportHexPalette,
    PST_OT_OpenShadingWorkspace,
    PST_OT_RefreshPaletteList,
    PST_OT_SyncPixelProcessor,
)
from .bake.baker import PST_OT_BakeToNewTexture
from .ui.panel import PST_PT_MainPanel
from .ui.panel_view3d import PST_PT_View3DQuickPanel

CLASSES = (
    PSTProperties,
    PST_OT_AddPixelProcessor,
    PST_OT_SyncPixelProcessor,
    PST_OT_OpenShadingWorkspace,
    PST_OT_ImportGPLPalette,
    PST_OT_ImportHexPalette,
    PST_OT_RefreshPaletteList,
    PST_OT_BakeToNewTexture,
    PST_PT_MainPanel,
    PST_PT_View3DQuickPanel,
)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.Scene.pst_settings = bpy.props.PointerProperty(type=PSTProperties)



def unregister():
    del bpy.types.Scene.pst_settings

    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
