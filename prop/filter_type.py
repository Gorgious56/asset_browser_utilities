from bpy.types import PropertyGroup
from bpy.props import BoolProperty, StringProperty

class FilterType(PropertyGroup):
    value: BoolProperty()
    icon: StringProperty()


def initialize_filter_types(filter_types):
    for name, (value, icon) in {
        "Actions": (False, "ACTION"),
        "Materials": (False, "MATERIAL"),
        "Objects": (True, "OBJECT_DATA"),
        "Worlds": (False, "WORLD"),
    }.items():
        new = filter_types.add()
        new.name = name
        new.value = value
        new.icon = icon
