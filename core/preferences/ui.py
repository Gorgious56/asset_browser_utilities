from bpy.types import AddonPreferences
from bpy.props import PointerProperty

from asset_browser_utilities.core.cache.prop import Cache


class AssetBrowserUtilitiesAddonPreferences(AddonPreferences):
    bl_idname = "asset_browser_utilities"

    cache: PointerProperty(type=Cache, options={"HIDDEN"})
