from bpy.types import AddonPreferences
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.core.cache.prop import Cache


class AssetBrowserUtilitiesAddonPreferences(AddonPreferences):
    bl_idname = "asset_browser_utilities"

    cache: PointerProperty(type=Cache, options={"HIDDEN"})
    defaults: PointerProperty(type=Cache)
    show_defaults: BoolProperty(name="Set Operator Defaults")
    show_custom_props: BoolProperty(
        default=True,
        name="Show Asset Custom Properties",
        description="Add a Panel in the Asset Browser interface to display asset custom properties",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "show_custom_props")

        self.defaults.asset_filter_settings.filter_selection.allow = True
        self.defaults.asset_filter_settings.filter_catalog_allow = True

        box = layout.box()
        box.prop(self, "show_defaults", toggle=True)
        if self.show_defaults:
            for attr in self.defaults.__annotations__:
                default_setting = getattr(self.defaults, attr)
                if hasattr(default_setting, "draw"):
                    default_setting.draw(box, context)
