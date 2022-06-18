from bpy.types import Menu
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_catalogs(Menu, ABUOperatorsMenu):
    bl_label = "Catalogs"
    ops_cmd = [
        ("abu.catalog_move", "Move To Catalog", "ADD"),
        ("abu.catalog_remove_from", "Remove From Catalog", "REMOVE"),
        ("abu.catalog_move_from_a_to_b", "Move From A to B", "FOLDER_REDIRECT"),
        ("abu.sort_catalogs_like_folders", "Create From Folders", "FILE_FOLDER"),
    ]
