import json
from pathlib import Path

from ..utils.math_utils import rgb_to_hex
from .gpl_parser import parse_gpl


class PaletteManager:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent
        self.presets_path = base_dir / "presets.json"
        self.custom_path = base_dir / "custom_presets.json"
        self._palettes = {}

    def ensure_loaded(self):
        if self._palettes:
            return self._palettes

        presets = self._load_json(self.presets_path)
        custom = self._load_json(self.custom_path)
        self._palettes = {**presets, **custom}
        return self._palettes

    def _load_json(self, path):
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def _save_custom(self):
        builtin = set(self._load_json(self.presets_path).keys())
        custom = {k: v for k, v in self._palettes.items() if k not in builtin}
        with open(self.custom_path, "w", encoding="utf-8") as handle:
            json.dump(custom, handle, ensure_ascii=False, indent=2)

    def refresh(self):
        self._palettes = {}
        return self.ensure_loaded()

    def add_palette(self, name, colors):
        cleaned = [c.upper() if c.startswith("#") else f"#{c.upper()}" for c in colors]
        if not cleaned:
            raise ValueError("Palette cannot be empty")
        self.ensure_loaded()
        self._palettes[name] = cleaned
        self._save_custom()

    def import_gpl(self, filepath):
        name, colors = parse_gpl(filepath)
        self.add_palette(name, colors)
        return name

    def import_hex_list(self, filepath):
        name = Path(filepath).stem
        colors = []
        with open(filepath, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                token = line.split()[0]
                if token.startswith("#") and len(token) == 7:
                    colors.append(token.upper())
                    continue
                if "," in token:
                    try:
                        rgb = tuple(float(x) for x in token.split(",")[:3])
                        colors.append(rgb_to_hex(rgb))
                    except ValueError:
                        pass

        self.add_palette(name, colors)
        return name


PALETTE_MANAGER = PaletteManager()
