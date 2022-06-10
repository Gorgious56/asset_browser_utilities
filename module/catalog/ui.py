from bpy.types import Menu
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_catalogs(Menu, ABUOperatorsMenu):
    bl_label = "Catalogs"

    def setup_ops(self, layout, context):
        self.add_op(layout, "abu.catalog_move", "Move To Catalog", "ADD")
        self.add_op(layout, "abu.catalog_remove_from", "Remove From Catalog", "REMOVE")
        self.add_op(layout, "abu.catalog_move_from_a_to_b", "Move From A to B", "FOLDER_REDIRECT")

        library_source_from_context = LibraryType.get_library_type_from_context(context)
        if library_source_from_context == LibraryType.UserLibrary.value:
            self.add_op(layout, "abu.sort_catalogs_like_folders", "Create From Folders", "FILE_FOLDER")
