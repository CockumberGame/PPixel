# Pixel Shader Toolkit for Blender

MVP scaffold of a commercial-oriented Blender add-on that lives in Shader Editor and inserts a non-destructive pixel/palette/dither processor node group into existing materials.

## Current modules

- `ui/` — panel and theme constants
- `core/` — properties, pipeline operators, node builder
- `palette/` — presets + import manager (`.gpl`/HEX list)
- `bake/` — bake to new texture operator
- `utils/` — math/color helpers

## Notes

- Non-destructive flow: the add-on creates its own node group and reconnects only the Principled BSDF Base Color chain.
- Works with material nodes (geometry complexity agnostic).
- Includes 131 ready palettes in `palette/presets.json`.

## Install

1. Zip the `pixel_shader_toolkit` folder.
2. Blender -> Edit -> Preferences -> Add-ons -> Install...
3. Enable **Pixel Shader Toolkit**.
4. Open Shader Editor sidebar -> **Pixel** tab.
