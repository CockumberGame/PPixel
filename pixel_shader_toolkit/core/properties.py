import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty
from bpy.types import PropertyGroup

from ..palette.manager import PALETTE_MANAGER


def palette_items(_self, _context):
    palettes = PALETTE_MANAGER.ensure_loaded()
    return [(name, name, f"Palette: {name}") for name in palettes.keys()]


class PSTProperties(PropertyGroup):
    pixel_size: FloatProperty(name="Pixel Size", default=64.0, min=1.0, max=1024.0)
    palette_name: EnumProperty(name="Palette", items=palette_items)
    palette_impact: FloatProperty(name="Palette Impact", default=1.0, min=0.0, max=1.0)

    dither_enabled: BoolProperty(name="Enable Dither", default=True)
    dither_strength: FloatProperty(name="Dither Strength", default=0.5, min=0.0, max=1.0)

    brightness: FloatProperty(name="Brightness", default=0.0, min=-1.0, max=1.0)
    exposure: FloatProperty(name="Exposure", default=0.0, min=-5.0, max=5.0)
    contrast: FloatProperty(name="Contrast", default=1.0, min=0.0, max=3.0)
    saturation: FloatProperty(name="Saturation", default=1.0, min=0.0, max=2.0)
    blur: FloatProperty(name="Blur", default=0.0, min=0.0, max=1.0)
    tint_r: FloatProperty(name="Tint R", default=1.0, min=0.0, max=2.0)
    tint_g: FloatProperty(name="Tint G", default=1.0, min=0.0, max=2.0)
    tint_b: FloatProperty(name="Tint B", default=1.0, min=0.0, max=2.0)

    bake_resolution: IntProperty(name="Bake Resolution", default=1024, min=128, max=2048)
    bake_image_name: StringProperty(name="Image Name", default="PST_Baked")
