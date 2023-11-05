import string

from bpy.types import PropertyGroup
from bpy.props import IntProperty

ALPHABET = string.ascii_lowercase + string.digits


class StrProperty(PropertyGroup):
    pass

class IntPropertyCollection(PropertyGroup):
    value: IntProperty(min=0)
    pass
