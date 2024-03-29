from bpy.types import Menu
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_assets(Menu, ABUOperatorsMenu):
    bl_label = "Assets"
    ops_cmd = [
        ("abu.asset_mark", "Mark", "SHADERFX"),
        ("abu.asset_unmark", "Unmark", "TRASH"),
        ("abu.asset_export", "Export", "EXPORT"),
        ("abu.asset_import", "Import", "IMPORT"),
        ("abu.asset_link", "Link", "LINKED"),
        ("abu.asset_link_relocate", "Relocate", "LIBRARY_DATA_BROKEN"),
        ("abu.asset_update", "Update", "FILE_REFRESH"),
        ("abu.asset_data_copy", "Copy From Active", "COPYDOWN"),
        ("abu.operation_custom", "Custom Operation(s)", "MODIFIER"),
    ]
