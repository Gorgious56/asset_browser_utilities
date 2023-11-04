from enum import Enum
import math
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.module.tag.tool import ensure_asset_has_uuid_tag, has_asset_tag_uuid


def get_triangle_count(asset, smart_tag):
    if not hasattr(asset, "data") or asset.data is None or not hasattr(asset.data, "vertices"):
        return ""
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
    if not hasattr(asset, "data") or asset.data is None or not hasattr(asset.data, "vertices"):
        return ""
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
    if not hasattr(asset, "dimensions"):
        return ""
    ret = "Dim. : "
    for i, axis in enumerate(("X", "Y", "Z")):
        ret += f"{round(asset.dimensions[i], 3)}m"
        if i < 2:
            ret += " * "
    return ret


def get_scale(asset, smart_tag):
    if not hasattr(asset, "scale"):
        return ""
    ret = "Scale : "
    for i, axis in enumerate(("X", "Y", "Z")):
        ret += f"{round(asset.scale[i], 3)}"
        if i < 2:
            ret += " * "
    return ret


def get_uuid(asset, smart_tag):
    if has_asset_tag_uuid(asset):
        return
    return ensure_asset_has_uuid_tag(asset).name


class SmartTag(Enum):
    CustomProperty = "Custom Property"
    Dimensions = "Dimensions"
    TriangleCount = "Triangle Count"
    Scale = "Scale"
    VertexCount = "Vertex Count"
    Uuid = "UUID"

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
        elif member == SmartTag.Uuid.value:
            return get_uuid


def apply_smart_tag(asset, smart_tag):
    asset_data = asset.asset_data
    asset_tags = asset_data.tags
    tag = SmartTag.operation(smart_tag.operation)(asset, smart_tag)
    if tag is not None and tag != "":
        asset_tags.new(str(tag), skip_if_exists=True)
        Logger.display(f"Added smart tag '{tag}' to '{asset.name}'")
