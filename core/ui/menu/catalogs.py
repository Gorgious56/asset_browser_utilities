from bpy.types import Menu
from .prop import FileMenu, LibraryMenu


class ABU_MT_library_catalogs(Menu, LibraryMenu):
    bl_label = "Catalogs"

    def draw(self, context):
        draw(self)


class ABU_MT_file_catalogs(Menu, FileMenu):
    bl_label = "Catalogs"

    def draw(self, context):
        draw(self)


def draw(self):
    mark_op = self.layout.operator("asset.batch_move_to_catalog", text="Move To Catalog", icon="ADD")
    mark_op.library_settings.this_file_only = not self.LIBRARY
    mark_op = self.layout.operator("asset.batch_remove_from_catalog", text="Remove From Catalog", icon="REMOVE")
    mark_op.library_settings.this_file_only = not self.LIBRARY
