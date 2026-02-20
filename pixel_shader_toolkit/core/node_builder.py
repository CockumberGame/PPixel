import bpy

GROUP_NAME = "PST_PixelProcessor"


def get_or_create_group():
    group = bpy.data.node_groups.get(GROUP_NAME)
    if group:
        return group

    group = bpy.data.node_groups.new(GROUP_NAME, "ShaderNodeTree")

    interface = group.interface
    interface.new_socket(name="Color In", in_out="INPUT", socket_type="NodeSocketColor")
    interface.new_socket(name="Pixel Size", in_out="INPUT", socket_type="NodeSocketFloat")
    interface.new_socket(name="Palette Impact", in_out="INPUT", socket_type="NodeSocketFloat")
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
    group_in.location = (-980, 0)
    group_out = nodes.new("NodeGroupOutput")
    group_out.location = (860, 0)

    tex_coord = nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-980, -240)

    vector_math_mul = nodes.new("ShaderNodeVectorMath")
    vector_math_mul.operation = "SCALE"
    vector_math_mul.location = (-780, -240)

    vector_math_floor = nodes.new("ShaderNodeVectorMath")
    vector_math_floor.operation = "FLOOR"
    vector_math_floor.location = (-580, -240)

    vector_math_div = nodes.new("ShaderNodeVectorMath")
    vector_math_div.operation = "DIVIDE"
    vector_math_div.location = (-380, -240)

    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-220, -440)
    noise.inputs[2].default_value = 16.0

    add_dither = nodes.new("ShaderNodeMath")
    add_dither.operation = "MULTIPLY"
    add_dither.location = (-20, -400)

    bright_contrast = nodes.new("ShaderNodeBrightContrast")
    bright_contrast.location = (-60, 140)

    exposure_mult = nodes.new("ShaderNodeMixRGB")
    exposure_mult.blend_type = "MULTIPLY"
    exposure_mult.location = (140, 140)
    exposure_mult.inputs[0].default_value = 1.0

    exposure_map = nodes.new("ShaderNodeMapRange")
    exposure_map.location = (-60, -80)
    exposure_map.inputs[1].default_value = -5.0
    exposure_map.inputs[2].default_value = 5.0
    exposure_map.inputs[3].default_value = 0.0
    exposure_map.inputs[4].default_value = 2.0

    hue_sat = nodes.new("ShaderNodeHueSaturation")
    hue_sat.location = (340, 140)

    tint_mul = nodes.new("ShaderNodeMixRGB")
    tint_mul.blend_type = "MULTIPLY"
    tint_mul.location = (540, 140)
    tint_mul.inputs[0].default_value = 1.0

    add_to_color = nodes.new("ShaderNodeMixRGB")
    add_to_color.blend_type = "ADD"
    add_to_color.location = (540, -40)
    add_to_color.inputs[0].default_value = 1.0

    blur_mix = nodes.new("ShaderNodeMixRGB")
    blur_mix.blend_type = "MIX"
    blur_mix.location = (700, 80)

    mix_palette = nodes.new("ShaderNodeMixRGB")
    mix_palette.blend_type = "MIX"
    mix_palette.location = (860, 80)

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

    links.new(group_in.outputs["Blur"], blur_mix.inputs[0])
    links.new(add_to_color.outputs[0], blur_mix.inputs[1])
    links.new(group_in.outputs["Color In"], blur_mix.inputs[2])

    links.new(group_in.outputs["Palette Impact"], mix_palette.inputs[0])
    links.new(blur_mix.outputs[0], mix_palette.inputs[1])
    links.new(group_in.outputs["Color In"], mix_palette.inputs[2])

    links.new(mix_palette.outputs[0], group_out.inputs["Color Out"])

    return group


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
    group_node.label = "Pixel Shader Toolkit"
    group_node.location = (bsdf.location.x - 280, bsdf.location.y)

    group_node.inputs["Pixel Size"].default_value = settings.pixel_size
    group_node.inputs["Palette Impact"].default_value = settings.palette_impact
    group_node.inputs["Dither Strength"].default_value = settings.dither_strength if settings.dither_enabled else 0.0
    group_node.inputs["Brightness"].default_value = settings.brightness
    group_node.inputs["Exposure"].default_value = settings.exposure
    group_node.inputs["Contrast"].default_value = settings.contrast
    group_node.inputs["Saturation"].default_value = settings.saturation
    group_node.inputs["Blur"].default_value = settings.blur
    group_node.inputs["Tint"].default_value = (settings.tint_r, settings.tint_g, settings.tint_b, 1.0)

    if existing_link:
        links.new(existing_link.from_socket, group_node.inputs["Color In"])
        links.remove(existing_link)

    links.new(group_node.outputs["Color Out"], base_input)

    return group_node
