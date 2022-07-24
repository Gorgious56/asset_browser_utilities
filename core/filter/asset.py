from bpy.types import PropertyGroup
from bpy.props import BoolProperty, EnumProperty


class FilterAssets(PropertyGroup):
    only_assets: BoolProperty(default=False)
