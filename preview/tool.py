import sys
import time
import numpy as np
from asset_browser_utilities.core.log.logger import Logger
import bpy


def can_preview_be_generated(asset):
    if isinstance(
        asset,
        (
            bpy.types.Action,
            bpy.types.Brush,
            bpy.types.Collection,
            bpy.types.ShaderNodeTree,
            bpy.types.Light,
            bpy.types.Material,
            # bpy.types.Scene,
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
    elif isinstance(asset, bpy.types.Image):
        return bool(asset.pixels)
    return False

def is_preview_generated(asset):
    preview = asset.preview
    now = time.time()
    if preview is None:
        is_preview_generated.start = now
        asset.asset_generate_preview()
        return False
    else:
        if not preview.image_pixels:
            return True
    arr = np.zeros((preview.image_size[0] * preview.image_size[1]) * 4, dtype=np.float32)
    preview.image_pixels_float.foreach_get(arr)
    are_the_any_pixels = np.any((arr != 0))
    took_too_long = now - is_preview_generated.start > 20
    if are_the_any_pixels or took_too_long:
        if took_too_long:
            Logger.display(f"Asset '{asset.name}' took too long to generate a preview. Aborting")
        else:
            Logger.display(f"Preview generated for '{asset.name}'")
        is_preview_generated.start = now
        return True
    return False

is_preview_generated.start = sys.maxsize

def create_image(name, width, height, alpha=True):
    img = bpy.data.images.new(name=name, width=width, height=height, alpha=alpha)
    return img
