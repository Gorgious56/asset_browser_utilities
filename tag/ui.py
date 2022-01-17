from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.prop import FileMenu, LibraryMenu


class ABU_MT_library_tags(Menu, LibraryMenu):
    bl_label = "Tags"

    def draw(self, context):
        draw_tags(self)


class ABU_MT_file_tags(Menu, FileMenu):
    bl_label = "Tags"

    def draw(self, context):
        draw_tags(self)


def draw_tags(self):
    add_tags_op = self.layout.operator("asset.batch_add_tags", text="Add", icon="ADD")
    add_tags_op.library_settings.this_file_only = not self.LIBRARY
    remove_tags_op = self.layout.operator("asset.batch_remove_tags", text="Remove", icon="REMOVE")
    remove_tags_op.library_settings.this_file_only = not self.LIBRARY
