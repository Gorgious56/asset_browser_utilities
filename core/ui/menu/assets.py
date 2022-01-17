from bpy.types import Menu
from .prop import FileMenu, LibraryMenu


class ABU_MT_library_assets(Menu, LibraryMenu):
    bl_label = "Assets"

    def draw(self, context):
        draw_mark_or_unmark(self)


class ABU_MT_file_assets(Menu, FileMenu):
    bl_label = "Assets"

    def draw(self, context):
        draw_mark_or_unmark(self)


def draw_mark_or_unmark(self):
    mark_op = self.layout.operator("asset.batch_mark", text="Mark", icon="SHADERFX")
    mark_op.library_settings.this_file_only = not self.LIBRARY
    unmark_op = self.layout.operator("asset.batch_unmark", text="Unmark", icon="TRASH")
    unmark_op.library_settings.this_file_only = not self.LIBRARY
