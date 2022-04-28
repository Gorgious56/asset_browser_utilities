from enum import Enum
from os.path import getsize
import math
from asset_browser_utilities.library.path import get_asset_filepath

import bpy
from bpy.types import PropertyGroup
from bpy.props import EnumProperty, StringProperty, IntProperty

from asset_browser_utilities.core.cache.tool import CacheMapping


def get_triangle_count(asset, smart_tag):
    if smart_tag.round_mode == "Up":
        op = math.ceil
        prefix = "< "
    else:
        op = math.floor
        prefix = "> "
    return (
        prefix
        + str(
            op(sum(len(polygon.vertices) - 2 for polygon in asset.data.polygons) / smart_tag.increment)
            * smart_tag.increment
        )
        + " Triangles"
        if hasattr(asset, "type") and asset.type == "MESH"
        else None
    )


def get_vertex_count(asset, smart_tag):
    if smart_tag.round_mode == "Up":
        op = math.ceil
        prefix = "< "
    else:
        op = math.floor
        prefix = "> "
    return (
        prefix + str(op((len(asset.data.vertices) / smart_tag.increment)) * smart_tag.increment) + " Vertices"
        if hasattr(asset, "type") and asset.type == "MESH"
        else None
    )


def get_dimensions(asset, smart_tag):
    ret = "Dim. : "
    for i, axis in enumerate(("X", "Y", "Z")):
        ret += f"{round(asset.dimensions[i], 3)}m"
        if i < 2:
            ret += " * "
    return ret


def get_scale(asset, smart_tag):
    ret = "Scale : "
    for i, axis in enumerate(("X", "Y", "Z")):
        ret += f"{round(asset.scale[i], 3)}"
        if i < 2:
            ret += " * "
    return ret


class SmartTag(Enum):
    CustomProperty = "Custom Property"
    Dimensions = "Dimensions"
    TriangleCount = "Triangle Count"
    Scale = "Scale"
    VertexCount = "Vertex Count"

    @staticmethod
    def operation(member):
        if member == SmartTag.TriangleCount.value:
            return get_triangle_count
        elif member == SmartTag.VertexCount.value:
            return get_vertex_count
        elif member == SmartTag.CustomProperty.value:
            return lambda asset, smart_tag: asset.get(smart_tag.custom_property_name, None)
        elif member == SmartTag.Dimensions.value:
            return get_dimensions
        elif member == SmartTag.Scale.value:
            return get_scale


class SmartTagPG(PropertyGroup, CacheMapping):
    CACHE_MAPPING = "smart_tag_settings"

    operation: EnumProperty(name="Operation", items=[(s_t.value,) * 3 for s_t in SmartTag])
    custom_property_name: StringProperty(name="Custom Property Name")
    increment: IntProperty(min=1, default=500, name="Increment")
    round_mode: EnumProperty(name="Round", items=(("Up",) * 3, ("Down",) * 3))

    def draw(self, layout, context=None):
        box = layout.box()
        box.label(text="Smart Tag")
        box.prop(self, "operation", text="")
        if self.operation == SmartTag.CustomProperty.value:
            box.prop(self, "custom_property_name")
        if self.operation in (SmartTag.TriangleCount.value, SmartTag.VertexCount.value):
            box.prop(self, "increment")
            box.prop(self, "round_mode")


def apply_smart_tag(asset, smart_tag):
    asset_data = asset.asset_data
    asset_tags = asset_data.tags
    tag = SmartTag.operation(smart_tag.operation)(asset, smart_tag)
    if tag is not None:
        asset_tags.new(str(tag), skip_if_exists=True)
