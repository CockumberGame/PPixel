import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty
from bpy.types import PropertyGroup

from ..palette.manager import PALETTE_MANAGER


def palette_items(_self, _context):
    palettes = PALETTE_MANAGER.ensure_loaded()
    return [(name, name, f"Palette: {name}") for name in palettes.keys()]


def on_settings_updated(self, context):
    if not context or not hasattr(context, "scene"):
        return

    from .node_builder import sync_active_material_nodes

    sync_active_material_nodes(context, self)


class PSTProperties(PropertyGroup):
    pixel_size: FloatProperty(name="Pixel Size", default=64.0, min=1.0, max=1024.0, update=on_settings_updated)
    palette_name: EnumProperty(name="Palette", items=palette_items, update=on_settings_updated)
    palette_impact: FloatProperty(name="Palette Impact", default=1.0, min=0.0, max=1.0, update=on_settings_updated)

    dither_enabled: BoolProperty(name="Enable Dither", default=True, update=on_settings_updated)
    dither_strength: FloatProperty(name="Dither Strength", default=0.5, min=0.0, max=1.0, update=on_settings_updated)

    brightness: FloatProperty(name="Brightness", default=0.0, min=-1.0, max=1.0, update=on_settings_updated)
    exposure: FloatProperty(name="Exposure", default=0.0, min=-5.0, max=5.0, update=on_settings_updated)
    contrast: FloatProperty(name="Contrast", default=1.0, min=0.0, max=3.0, update=on_settings_updated)
    saturation: FloatProperty(name="Saturation", default=1.0, min=0.0, max=2.0, update=on_settings_updated)
    blur: FloatProperty(name="Blur", default=0.0, min=0.0, max=1.0, update=on_settings_updated)
    tint_r: FloatProperty(name="Tint R", default=1.0, min=0.0, max=2.0, update=on_settings_updated)
    tint_g: FloatProperty(name="Tint G", default=1.0, min=0.0, max=2.0, update=on_settings_updated)
    tint_b: FloatProperty(name="Tint B", default=1.0, min=0.0, max=2.0, update=on_settings_updated)

    bake_resolution: IntProperty(name="Bake Resolution", default=1024, min=128, max=2048)
    bake_image_name: StringProperty(name="Image Name", default="PST_Baked")
