from pathlib import Path


def parse_gpl(path):
    palette_name = Path(path).stem
    colors = []

    with open(path, "r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.lower().startswith("gimp palette"):
                continue
            if line.lower().startswith("name:"):
                palette_name = line.split(":", 1)[1].strip() or palette_name
                continue
            if line.lower().startswith("columns:"):
                continue

            parts = line.split()
            if len(parts) < 3:
                continue

            try:
                r, g, b = (int(parts[0]), int(parts[1]), int(parts[2]))
            except ValueError:
                continue

            colors.append(f"#{r:02X}{g:02X}{b:02X}")

    if not colors:
        raise ValueError(f"No colors found in GPL file: {path}")

    return palette_name, colors
