from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.prop import FileMenu, LibraryMenu


class ABU_MT_library_author(Menu, LibraryMenu):
    bl_label = "Author"

    def draw(self, context):
        draw(self)


class ABU_MT_file_author(Menu, FileMenu):
    bl_label = "Author"

    def draw(self, context):
        draw(self)


def draw(self):
    mark_op = self.layout.operator("asset.batch_add_author", text="Set", icon="ADD")
    mark_op.library_settings.this_file_only = not self.LIBRARY
    # mark_op = self.layout.operator("asset.batch_remove_author", text="Remove From Catalog", icon="REMOVE")
    # mark_op.library_settings.this_file_only = not self.LIBRARY
