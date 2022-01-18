from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.helper import is_library


class ABU_MT_previews(Menu):
    bl_label = "Previews"

    def draw(self, context):
        layout = self.layout
        this_file_only = not is_library(context)
        op = layout.operator("asset.batch_generate_previews", text="Generate", icon="FILE_REFRESH")
        op.library_settings.this_file_only = this_file_only
        layout.operator("asset.load_previews_from_disk", text="Load From Disk", icon="IMPORT")
