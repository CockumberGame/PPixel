import bpy

GROUP_NAME = "PST_PixelProcessor"
NODE_LABEL = "Pixel Shader Toolkit"


def get_or_create_group():
    group = bpy.data.node_groups.get(GROUP_NAME)
    if group:
        return group

    group = bpy.data.node_groups.new(GROUP_NAME, "ShaderNodeTree")

    interface = group.interface
    interface.new_socket(name="Color In", in_out="INPUT", socket_type="NodeSocketColor")
    interface.new_socket(name="Pixel Size", in_out="INPUT", socket_type="NodeSocketFloat")
    interface.new_socket(name="Palette Impact", in_out="INPUT", socket_type="NodeSocketFloat")
    interface.new_socket(name="Palette Levels", in_out="INPUT", socket_type="NodeSocketFloat")
    interface.new_socket(name="Dither Strength", in_out="INPUT", socket_type="NodeSocketFloat")
    interface.new_socket(name="Brightness", in_out="INPUT", socket_type="NodeSocketFloat")
    interface.new_socket(name="Exposure", in_out="INPUT", socket_type="NodeSocketFloat")
    interface.new_socket(name="Contrast", in_out="INPUT", socket_type="NodeSocketFloat")
    interface.new_socket(name="Saturation", in_out="INPUT", socket_type="NodeSocketFloat")
    interface.new_socket(name="Blur", in_out="INPUT", socket_type="NodeSocketFloat")
    interface.new_socket(name="Tint", in_out="INPUT", socket_type="NodeSocketColor")
    interface.new_socket(name="Color Out", in_out="OUTPUT", socket_type="NodeSocketColor")

    nodes = group.nodes
    links = group.links

    group_in = nodes.new("NodeGroupInput")
    group_in.location = (-1120, 0)
    group_out = nodes.new("NodeGroupOutput")
    group_out.location = (1380, 0)

    tex_coord = nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-1120, -300)

    vector_math_mul = nodes.new("ShaderNodeVectorMath")
    vector_math_mul.operation = "SCALE"
    vector_math_mul.location = (-900, -300)

    vector_math_floor = nodes.new("ShaderNodeVectorMath")
    vector_math_floor.operation = "FLOOR"
    vector_math_floor.location = (-680, -300)

    vector_math_div = nodes.new("ShaderNodeVectorMath")
    vector_math_div.operation = "DIVIDE"
    vector_math_div.location = (-460, -300)

    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-240, -420)
    noise.inputs[2].default_value = 16.0

    add_dither = nodes.new("ShaderNodeMath")
    add_dither.operation = "MULTIPLY"
    add_dither.location = (-20, -420)

    bright_contrast = nodes.new("ShaderNodeBrightContrast")
    bright_contrast.location = (-120, 200)

    exposure_mult = nodes.new("ShaderNodeMixRGB")
    exposure_mult.blend_type = "MULTIPLY"
    exposure_mult.location = (100, 200)
    exposure_mult.inputs[0].default_value = 1.0

    exposure_map = nodes.new("ShaderNodeMapRange")
    exposure_map.location = (-120, -40)
    exposure_map.inputs[1].default_value = -5.0
    exposure_map.inputs[2].default_value = 5.0
    exposure_map.inputs[3].default_value = 0.0
    exposure_map.inputs[4].default_value = 2.0

    hue_sat = nodes.new("ShaderNodeHueSaturation")
    hue_sat.location = (320, 200)

    tint_mul = nodes.new("ShaderNodeMixRGB")
    tint_mul.blend_type = "MULTIPLY"
    tint_mul.location = (540, 200)
    tint_mul.inputs[0].default_value = 1.0

    add_to_color = nodes.new("ShaderNodeMixRGB")
    add_to_color.blend_type = "ADD"
    add_to_color.location = (760, 120)
    add_to_color.inputs[0].default_value = 1.0

    separate = nodes.new("ShaderNodeSeparateColor")
    separate.location = (760, 320)

    levels_minus_one = nodes.new("ShaderNodeMath")
    levels_minus_one.operation = "SUBTRACT"
    levels_minus_one.location = (760, -120)
    levels_minus_one.inputs[1].default_value = 1.0

    channels = []
    y = 360
    for channel_name in ("Red", "Green", "Blue"):
        mul = nodes.new("ShaderNodeMath")
        mul.operation = "MULTIPLY"
        mul.location = (980, y)

        rnd = nodes.new("ShaderNodeMath")
        rnd.operation = "ROUND"
        rnd.location = (1160, y)

        div = nodes.new("ShaderNodeMath")
        div.operation = "DIVIDE"
        div.location = (1340, y)

        channels.append((channel_name, mul, rnd, div))
        y -= 160

    combine = nodes.new("ShaderNodeCombineColor")
    combine.location = (1540, 220)

    blur_mix = nodes.new("ShaderNodeMixRGB")
    blur_mix.blend_type = "MIX"
    blur_mix.location = (1740, 120)

    mix_palette = nodes.new("ShaderNodeMixRGB")
    mix_palette.blend_type = "MIX"
    mix_palette.location = (1960, 120)

    links.new(group_in.outputs["Color In"], bright_contrast.inputs[0])
    links.new(group_in.outputs["Brightness"], bright_contrast.inputs[1])
    links.new(group_in.outputs["Contrast"], bright_contrast.inputs[2])

    links.new(group_in.outputs["Exposure"], exposure_map.inputs[0])
    links.new(exposure_map.outputs[0], exposure_mult.inputs[2])
    links.new(bright_contrast.outputs[0], exposure_mult.inputs[1])

    links.new(exposure_mult.outputs[0], hue_sat.inputs[4])
    links.new(group_in.outputs["Saturation"], hue_sat.inputs[1])

    links.new(hue_sat.outputs[0], tint_mul.inputs[1])
    links.new(group_in.outputs["Tint"], tint_mul.inputs[2])

    links.new(tex_coord.outputs["UV"], vector_math_mul.inputs[0])
    links.new(group_in.outputs["Pixel Size"], vector_math_mul.inputs[3])
    links.new(vector_math_mul.outputs[0], vector_math_floor.inputs[0])
    links.new(vector_math_floor.outputs[0], vector_math_div.inputs[0])
    links.new(vector_math_mul.inputs[3], vector_math_div.inputs[1])

    links.new(vector_math_div.outputs[0], noise.inputs[0])
    links.new(noise.outputs[0], add_dither.inputs[0])
    links.new(group_in.outputs["Dither Strength"], add_dither.inputs[1])

    links.new(tint_mul.outputs[0], add_to_color.inputs[1])
    links.new(add_dither.outputs[0], add_to_color.inputs[2])

    links.new(group_in.outputs["Palette Levels"], levels_minus_one.inputs[0])

    links.new(add_to_color.outputs[0], separate.inputs[0])

    for channel_name, mul, rnd, div in channels:
        links.new(separate.outputs[channel_name], mul.inputs[0])
        links.new(levels_minus_one.outputs[0], mul.inputs[1])
        links.new(mul.outputs[0], rnd.inputs[0])
        links.new(rnd.outputs[0], div.inputs[0])
        links.new(levels_minus_one.outputs[0], div.inputs[1])

    links.new(channels[0][3].outputs[0], combine.inputs["Red"])
    links.new(channels[1][3].outputs[0], combine.inputs["Green"])
    links.new(channels[2][3].outputs[0], combine.inputs["Blue"])

    links.new(group_in.outputs["Blur"], blur_mix.inputs[0])
    links.new(combine.outputs[0], blur_mix.inputs[1])
    links.new(group_in.outputs["Color In"], blur_mix.inputs[2])

    links.new(group_in.outputs["Palette Impact"], mix_palette.inputs[0])
    links.new(blur_mix.outputs[0], mix_palette.inputs[1])
    links.new(group_in.outputs["Color In"], mix_palette.inputs[2])

    links.new(mix_palette.outputs[0], group_out.inputs["Color Out"])

    return group


def _palette_levels(settings):
    from ..palette.manager import PALETTE_MANAGER

    palettes = PALETTE_MANAGER.ensure_loaded()
    colors = palettes.get(settings.palette_name, [])
    return float(max(2, min(256, len(colors))))


def apply_settings_to_node(group_node, settings):
    group_node.inputs["Pixel Size"].default_value = settings.pixel_size
    group_node.inputs["Palette Impact"].default_value = settings.palette_impact
    group_node.inputs["Palette Levels"].default_value = _palette_levels(settings)
    group_node.inputs["Dither Strength"].default_value = settings.dither_strength if settings.dither_enabled else 0.0
    group_node.inputs["Brightness"].default_value = settings.brightness
    group_node.inputs["Exposure"].default_value = settings.exposure
    group_node.inputs["Contrast"].default_value = settings.contrast
    group_node.inputs["Saturation"].default_value = settings.saturation
    group_node.inputs["Blur"].default_value = settings.blur
    group_node.inputs["Tint"].default_value = (settings.tint_r, settings.tint_g, settings.tint_b, 1.0)


def iter_pst_nodes(material):
    if not material or not material.use_nodes:
        return []
    return [
        node
        for node in material.node_tree.nodes
        if node.type == "GROUP" and node.node_tree and node.node_tree.name == GROUP_NAME
    ]


def sync_active_material_nodes(context, settings):
    obj = context.object
    if not obj or not obj.active_material:
        return 0

    nodes = iter_pst_nodes(obj.active_material)
    for node in nodes:
        apply_settings_to_node(node, settings)
    return len(nodes)


def attach_processor(material, settings):
    if not material or not material.use_nodes:
        raise ValueError("Select a material with nodes enabled")

    tree = material.node_tree
    nodes = tree.nodes
    links = tree.links

    output = next((n for n in nodes if n.type == "OUTPUT_MATERIAL" and n.is_active_output), None)
    bsdf = next((n for n in nodes if n.type == "BSDF_PRINCIPLED"), None)

    if not output or not bsdf:
        raise ValueError("Material must contain Material Output and Principled BSDF")

    base_input = bsdf.inputs.get("Base Color")
    existing_link = base_input.links[0] if base_input.links else None

    group_node = nodes.new("ShaderNodeGroup")
    group_node.node_tree = get_or_create_group()
    group_node.label = NODE_LABEL
    group_node.location = (bsdf.location.x - 280, bsdf.location.y)

    apply_settings_to_node(group_node, settings)

    if existing_link:
        links.new(existing_link.from_socket, group_node.inputs["Color In"])
        links.remove(existing_link)

    links.new(group_node.outputs["Color Out"], base_input)

    return group_node
