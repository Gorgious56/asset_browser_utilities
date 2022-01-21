from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType


class ABU_MT_previews(Menu):
    bl_label = "Previews"

    def draw(self, context):
        layout = self.layout
        library_type = LibraryType.get(context)
        op = layout.operator("asset.batch_generate_previews", text="Generate", icon="FILE_REFRESH")
        op.library_settings.library_type = library_type
        if library_type == LibraryType.FileCurrent.value:
            layout.operator("asset.load_previews_from_disk", text="Load From Disk", icon="IMPORT")
