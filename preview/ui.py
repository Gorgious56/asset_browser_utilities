from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.prop import FileMenu, LibraryMenu


class ABU_MT_library_previews(Menu, LibraryMenu):
    bl_label = "Previews"

    def draw(self, context):
        draw_batch_generate_previews(self)
        draw_previews(self)


class ABU_MT_file_previews(Menu, FileMenu):
    bl_label = "Previews"

    def draw(self, context):
        draw_batch_generate_previews(self)
        draw_previews(self)


def draw_batch_generate_previews(self):
    op = self.layout.operator("asset.batch_generate_previews", text="Generate", icon="FILE_REFRESH")
    op.library_settings.this_file_only = not self.LIBRARY


def draw_previews(self):
    self.layout.operator("asset.load_previews_from_disk", text="Load From Disk", icon="IMPORT")
