from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_assets(Menu, ABUOperatorsMenu):
    bl_label = "Assets"

    def setup_ops(self, layout, context):
        library_source_from_context = LibraryType.get_library_type_from_context(context)
        self.add_op(layout, "asset.batch_mark", "Mark", "SHADERFX")
        self.add_op(layout, "asset.batch_unmark", "Unmark", "TRASH")
        if library_source_from_context == LibraryType.FileCurrent.value:
            layout.operator("asset.batch_export", text="Export", icon="EXPORT")
            self.add_op(layout, "abu.copy_from_active", "Copy From Active", "COPYDOWN")
        else:
            self.add_op(layout, "asset.batch_import", "Import", "IMPORT")
        self.add_op(layout, "asset.batch_operate", "Custom Operation", "MODIFIER")
