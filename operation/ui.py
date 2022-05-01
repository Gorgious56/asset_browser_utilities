from bpy.types import Menu
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu
from asset_browser_utilities.library.prop import LibraryType


class ABU_MT_operations(Menu, ABUOperatorsMenu):
    bl_label = "Operations"

    def setup_ops(self, layout, context):
        self.add_op(layout, "asset.batch_operate", "Custom Operation", "MODIFIER")
        library_source_from_context = LibraryType.get_library_type_from_context(context)
        if library_source_from_context == LibraryType.FileCurrent.value:
            self.add_op(layout, "abu.copy_from_active", "Copy From Active", "COPYDOWN")
