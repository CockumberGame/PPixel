# Pixel Shader Toolkit for Blender

Commercial-oriented Blender add-on scaffold that inserts a non-destructive pixel/palette/dither processor node group into existing materials.

## Blender 5 compatibility & install

This repo now includes a **`blender_manifest.toml`** for Blender 5.0 extension installation flow.

Install options:
1. **Extensions** (Blender 5+): install zip containing `blender_manifest.toml` + `pixel_shader_toolkit/`.
2. **Legacy Add-ons**: install zip with `pixel_shader_toolkit/__init__.py` package.

## Where to find it in Blender

- **3D Viewport**: press **N** -> tab **Pixel Toolkit** (quick panel + shortcut to Shading workspace).
- **Shader Editor**: press **N** -> tab **Pixel Toolkit** (full controls).

## Design constraints (important)

Blender add-ons do **not** support arbitrary custom UI frameworks in sidebar panels. You can style by:
- layout composition (boxes, rows, headers),
- iconography,
- control sizing (`scale_y`),
- custom preview icons/images.

You cannot inject full CSS-like theming into native Blender panel widgets.

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

## Roadmap status (realistic)

Implemented now:
- panel + quick access UX,
- non-destructive insertion,
- controls sync,
- palette import/base management,
- base bake operator.

Still required for full commercial target:
- true nearest-color palette mapping (current stage is level-based quantization),
- ordered Bayer matrix modes (4x4/8x8),
- higher-fidelity blur path and performance tuning,
- robust batch workflow + QA test matrix on multiple Blender versions.
