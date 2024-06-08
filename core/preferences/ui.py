from bpy.types import AddonPreferences
from bpy.props import PointerProperty, BoolProperty, CollectionProperty, IntProperty

from asset_browser_utilities.core.cache.prop import Cache


class AssetBrowserUtilitiesAddonPreferences(AddonPreferences):
    bl_idname = "asset_browser_utilities"

    cache: PointerProperty(type=Cache, options={"HIDDEN"})
    defaults: PointerProperty(type=Cache)
    presets: CollectionProperty(type=Cache)
    save_compress: BoolProperty(
        default=True,
        name="Compress Files On Save",
        description="Automatically compress the file on save. This will reduce the file size on disk at the cost of extra computation",
    )
    verbose: BoolProperty(
        name="Verbose Output",
        description="Check this to get some information in the system console",
        default=True,
    )
    max_threads: IntProperty(default=8, min=1, soft_max=48, name="Maximum number of threads", description="This number of files will be launched concurrently when batch-executing on external files. The optimal number highly depends on the specifics of your machine. Don't set it too high or your computer will freeze.")

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "verbose", icon="INFO")
        layout.prop(self, "save_compress", icon="FILE_BLEND")
        layout.prop(self, "max_threads", icon="COLLAPSEMENU")

        self.defaults.asset_filter_settings.filter_selection.allow = True
        self.defaults.asset_filter_settings.filter_catalog.allow = False

        box = layout.box()
        self.defaults.draw(box, context, header="Expand Defaults Settings")

        box = layout.box()
        row = box.row(align=True)
        row.label(text="Presets")
        row.operator("abu.presets_add_or_remove", text="", icon="ADD").index = -1
        for i, preset in enumerate(self.presets):
            layout = box if preset.show else box.row(align=True)
            preset.draw(layout, context, header="Expand", rename=True)
            if not preset.show:
                layout.operator("abu.presets_add_or_remove", text="", icon="REMOVE").index = i
