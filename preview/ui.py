from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_previews(Menu, ABUOperatorsMenu):
    bl_label = "Previews"

    def setup_ops(self, layout, context):
        self.add_op(layout, "asset.batch_generate_previews", "Generate", "FILE_REFRESH")
        self.add_op(layout, "asset.load_previews_from_disk", "Load From Disk", "IMPORT")
        library_source_from_context = LibraryType.get_library_type_from_context(context)
        if library_source_from_context == LibraryType.FileCurrent.value:
            layout.operator("abu.previews_extract", text="Extract to Disk", icon="EXPORT")
