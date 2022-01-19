from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType


class ABU_MT_previews(Menu):
    bl_label = "Previews"

    def draw(self, context):
        layout = self.layout
        this_file_only = LibraryType.get(context)
        op = layout.operator("asset.batch_generate_previews", text="Generate", icon="FILE_REFRESH")
        op.library_settings.this_file_only = this_file_only
        layout.operator("asset.load_previews_from_disk", text="Load From Disk", icon="IMPORT")
