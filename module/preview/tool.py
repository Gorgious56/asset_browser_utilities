import sys
import time
import numpy as np
from asset_browser_utilities.core.log.logger import Logger
import bpy


INTERVAL_PREVIEW = 0.05


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


def create_image(name, width, height, alpha=True):
    img = bpy.data.images.new(name=name, width=width, height=height, alpha=alpha)
    return img
