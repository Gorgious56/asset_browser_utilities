from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType


class ABU_MT_description(Menu):
    bl_label = "Description"

    def draw(self, context):
        library_type = LibraryType.get(context)
        mark_op = self.layout.operator("asset.batch_set_description", text="Set", icon="ADD")
        mark_op.library_settings.library_type = library_type
