from bpy.types import PropertyGroup
from bpy.props import StringProperty


class CatalogExportSettings(PropertyGroup):
    path: StringProperty()
