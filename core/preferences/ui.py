from bpy.types import AddonPreferences
from bpy.props import PointerProperty, BoolProperty, CollectionProperty

from asset_browser_utilities.core.cache.prop import Cache


class AssetBrowserUtilitiesAddonPreferences(AddonPreferences):
    bl_idname = "asset_browser_utilities"

    cache: PointerProperty(type=Cache, options={"HIDDEN"})
    defaults: PointerProperty(type=Cache)
    presets: CollectionProperty(type=Cache)
    show_custom_props: BoolProperty(
        default=True,
        name="Show Asset Custom Properties",
        description="Add a Panel in the Asset Browser interface to display asset custom properties",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "show_custom_props")

        self.defaults.asset_filter_settings.filter_selection.allow = True
        self.defaults.asset_filter_settings.filter_catalog.allow = True

        box = layout.box()
        self.defaults.draw(box, context, header="Set Defaults")

        box = layout.box()
        row = box.row(align=True)
        row.label(text="Presets")
        row.operator("abu.presets_add_or_remove", text="", icon="ADD").index = -1
        for i, preset in enumerate(self.presets):
            lay = box if preset.show else box.row(align=True)
            preset.draw(lay, context, header="Expand", rename=True)
            if not preset.show:
                lay.operator("abu.presets_add_or_remove", text="", icon="REMOVE").index = i
