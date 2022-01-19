from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType


class ABU_MT_author(Menu):
    bl_label = "Author"

    def draw(self, context):
        layout = self.layout
        mark_op = layout.operator("asset.batch_set_author", text="Set", icon="ADD")
        mark_op.library_settings.this_file_only = LibraryType.get(context)
