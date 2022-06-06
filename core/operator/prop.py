from bpy.types import PropertyGroup
from bpy.props import StringProperty


class CurrentOperatorProperty(PropertyGroup):
    class_name: StringProperty()
