# Pixel Shader Toolkit for Blender

Commercial-oriented Blender add-on scaffold that inserts a non-destructive pixel/palette/dither processor node group into existing materials.

## Where to find it in Blender

- **3D Viewport**: press **N** -> tab **Pixel Toolkit** (quick panel + shortcut to Shading workspace).
- **Shader Editor**: press **N** -> tab **Pixel Toolkit** (full controls).

## Current modules

- `ui/` — Shader Editor panel + Viewport quick panel + theme constants
- `core/` — properties, pipeline operators, node builder, live settings sync
- `palette/` — presets + import manager (`.gpl`/HEX list)
- `bake/` — bake to new texture operator
- `utils/` — math/color helpers

## Notes

- Non-destructive flow: add-on creates its own node group and reconnects only the Principled BSDF Base Color chain.
- Works with material nodes (geometry complexity agnostic).
- Includes 131 ready palettes in `palette/presets.json`.

## Install

1. Zip the `pixel_shader_toolkit` folder.
2. Blender -> Edit -> Preferences -> Add-ons -> Install...
3. Enable **Pixel Shader Toolkit**.
4. Open **N-panel** in 3D View or Shader Editor and choose **Pixel Toolkit** tab.
