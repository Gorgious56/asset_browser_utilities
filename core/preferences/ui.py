import bpy
from bpy.types import AddonPreferences
from bpy.props import PointerProperty

from .prop import Cache


class AssetBrowserUtilitiesAddonPreferences(AddonPreferences):
    bl_idname = "asset_browser_utilities"

    cache_operator: PointerProperty(type=Cache)

    def draw(self, context):
        pass
