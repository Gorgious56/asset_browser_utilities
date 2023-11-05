import string

from bpy.types import PropertyGroup

ALPHABET = string.ascii_lowercase + string.digits


class StrProperty(PropertyGroup):
    pass
