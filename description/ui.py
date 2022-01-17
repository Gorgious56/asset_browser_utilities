from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.prop import FileMenu, LibraryMenu


class ABU_MT_library_description(Menu, LibraryMenu):
    bl_label = "Description"

    def draw(self, context):
        draw(self)


class ABU_MT_file_description(Menu, FileMenu):
    bl_label = "Description"

    def draw(self, context):
        draw(self)


def draw(self):
    mark_op = self.layout.operator("asset.batch_add_description", text="Set", icon="ADD")
    mark_op.library_settings.this_file_only = not self.LIBRARY
