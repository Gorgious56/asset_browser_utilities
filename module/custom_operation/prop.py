import bpy  # Do not remove even if it seems unused !!
from bpy.types import PropertyGroup
from bpy.props import (
    EnumProperty,
    BoolProperty,
    FloatVectorProperty,
    IntProperty,
    StringProperty,
)
from .tool import get_available_operations, get_enum_items


class OperationSetting(PropertyGroup):
    type: EnumProperty(
        name="Operation",
        items=lambda self, context: [(op.MAPPING, op.LABEL, op.DESCRIPTION) for op in get_available_operations()],
    )
    vector_value: FloatVectorProperty(name="Value")
    int_value: IntProperty(name="Value")
    bool_value: BoolProperty(name="Value")
    enum_value: EnumProperty(items=get_enum_items)
    string_value: StringProperty(name="Value")
    string_value_2: StringProperty(name="Value")
