from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType


class ABU_MT_previews(Menu):
    bl_label = "Previews"

    def draw(self, context):
        layout = self.layout
        library_source_from_context = LibraryType.get_library_type_from_context(context)
        op = layout.operator("asset.batch_generate_previews", text="Generate", icon="FILE_REFRESH")
        op.library_settings.source = library_source_from_context
        if library_source_from_context == LibraryType.FileCurrent.value:
            layout.operator("asset.load_previews_from_disk", text="Load From Disk", icon="IMPORT")
