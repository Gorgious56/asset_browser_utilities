from bpy.types import Menu
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_previews(Menu, ABUOperatorsMenu):
    bl_label = "Previews"

    def setup_ops(self, layout, context):
        self.add_op(layout, "abu.preview_generate", "Generate", "FILE_REFRESH")
        self.add_op(layout, "abu.preview_import", "Load From Disk", "IMPORT")
        library_source_from_context = LibraryType.get_library_type_from_context(context)
        if library_source_from_context == LibraryType.FileCurrent.value:
            layout.operator("abu.preview_extract", text="Extract to Disk", icon="EXPORT")
