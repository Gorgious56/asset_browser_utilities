import numpy as np
import bpy


def can_preview_be_generated(asset):
    if isinstance(
        asset,
        (
            bpy.types.Action,
            bpy.types.Brush,
            bpy.types.Collection,
            bpy.types.ShaderNodeTree,
            bpy.types.Image,
            bpy.types.Light,
            bpy.types.Material,
            bpy.types.Scene,
            bpy.types.Screen,
            bpy.types.Texture,
            bpy.types.World,
        ),
    ):
        return True
    elif isinstance(asset, bpy.types.Object):
        if asset.type in ("MESH", "FONT", "LIGHT", "GREASEPENCIL", "SURFACE", "META"):
            if asset.type == "MESH" and len(asset.data.polygons) == 0:
                return False
            return True
    return False


def is_preview_generated(asset):
    preview = asset.preview
    if preview is None:
        asset.asset_generate_preview()
    else:
        if not preview.image_pixels:
            return True
    arr = np.zeros((preview.image_size[0] * preview.image_size[1]) * 4, dtype=np.float32)
    preview.image_pixels_float.foreach_get(arr)
    return np.any((arr != 0))
