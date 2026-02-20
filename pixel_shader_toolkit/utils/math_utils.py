def clamp(value, min_value=0.0, max_value=1.0):
    return max(min_value, min(max_value, value))


def hex_to_rgb(hex_color):
    normalized = hex_color.strip().lstrip("#")
    if len(normalized) != 6:
        raise ValueError(f"Unsupported HEX color: {hex_color}")

    return tuple(int(normalized[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    channels = [int(clamp(channel) * 255) for channel in rgb]
    return f"#{channels[0]:02X}{channels[1]:02X}{channels[2]:02X}"
