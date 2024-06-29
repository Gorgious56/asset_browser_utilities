import sys
import time
import numpy as np
from asset_browser_utilities.core.log.logger import Logger
import bpy


INTERVAL_PREVIEW = 0.05


def ensure_diffuse_texture_is_selected(asset):
    if getattr(asset, "data", None) is None or not hasattr(asset.data, "materials"):
        return
    for mat in asset.data.materials:
        if mat.use_nodes:
            nodes = mat.node_tree.nodes
            output_node = next(n for n in nodes if n.type == "OUTPUT_MATERIAL")
            surface_input = output_node.inputs["Surface"]
            if surface_input.links:
                shader = surface_input.links[0].from_node
                shader_inputs = shader.inputs
                links = None
                try:
                    links = shader_inputs["Base Color"].links
                except KeyError:
                    try:
                        links = shader_inputs["Color"].links
                    except KeyError:
                        pass
                if links:
                    diffuse_texture_node = links[0].from_node
                    nodes.active = diffuse_texture_node


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
