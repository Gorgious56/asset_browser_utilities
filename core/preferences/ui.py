from bpy.types import AddonPreferences
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.core.cache.prop import Cache


class AssetBrowserUtilitiesAddonPreferences(AddonPreferences):
    bl_idname = "asset_browser_utilities"

    cache: PointerProperty(type=Cache, options={"HIDDEN"})
    show_custom_props: BoolProperty(
        default=True,
        name="Show Asset Custom Properties",
        description="Add a Panel in the Asset Browser interface to display asset custom properties",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "show_custom_props")
