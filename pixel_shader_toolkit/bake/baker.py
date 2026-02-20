import bpy
from bpy.types import Operator


class PST_OT_BakeToNewTexture(Operator):
    bl_idname = "pst.bake_to_new_texture"
    bl_label = "Bake to New Texture"
    bl_description = "Bake the current material result into a new image"

    def execute(self, context):
        scene = context.scene
        settings = scene.pst_settings
        obj = context.object
        if not obj or not obj.active_material:
            self.report({"ERROR"}, "Select object with active material")
            return {"CANCELLED"}

        material = obj.active_material
        if not material.use_nodes:
            self.report({"ERROR"}, "Material nodes are required")
            return {"CANCELLED"}

        image = bpy.data.images.new(
            settings.bake_image_name,
            width=settings.bake_resolution,
            height=settings.bake_resolution,
            alpha=True,
        )

        node_tree = material.node_tree
        image_node = node_tree.nodes.new("ShaderNodeTexImage")
        image_node.image = image
        node_tree.nodes.active = image_node

        prev_engine = scene.render.engine
        prev_bake_type = scene.cycles.bake_type if hasattr(scene, "cycles") else None

        try:
            scene.render.engine = "CYCLES"
            if hasattr(scene, "cycles"):
                scene.cycles.bake_type = "DIFFUSE"
            bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"})
            image.pack()
        except RuntimeError as exc:
            self.report({"ERROR"}, f"Bake failed: {exc}")
            return {"CANCELLED"}
        finally:
            scene.render.engine = prev_engine
            if prev_bake_type and hasattr(scene, "cycles"):
                scene.cycles.bake_type = prev_bake_type

        self.report({"INFO"}, f"Baked image created: {image.name}")
        return {"FINISHED"}
