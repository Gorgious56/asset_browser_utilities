import bpy


def decimate(obj, tris, apply):
    mod_name = "ABU_DECIMATE"
    mod = obj.modifiers.new(type="DECIMATE", name=mod_name)
    mod.ratio = tris / len(obj.data.polygons)
    if apply:
        if bpy.app.version >= (3, 2, 0):
            with bpy.context.temp_override(object=obj, view_layer=bpy.context.view_layer, scene=bpy.context.scene):
                bpy.ops.object.modifier_apply(modifier=mod.name)
        else:
            bpy.ops.object.modifier_apply(
                {"object": obj, "view_layer": bpy.context.view_layer, "scene": bpy.context.scene}, modifier=mod.name
            )


class DecimateOperation:
    MAPPING = "DECIMATE"
    LABEL = "Decimate"
    DESCRIPTION = "Decimate the mesh (only applicable on mesh objects)"
    OPERATION = lambda assets, tris, apply: [
        decimate(a, tris, apply) for a in assets if hasattr(a, "type") and a.type == "MESH"
    ]
    ATTRIBUTES = ("int_value", "bool_value")
    ATTRIBUTES_NAMES = ("Number of Triangles (Half if quad-based)", "Apply Modifier")
