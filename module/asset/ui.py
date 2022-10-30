from bpy.types import Menu
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_assets(Menu, ABUOperatorsMenu):
    bl_label = "Assets"
    ops_cmd = [
        ("abu.mark", "Mark", "SHADERFX"),
        ("abu.unmark", "Unmark", "TRASH"),
        ("abu.batch_export", "Export", "EXPORT"),
        ("abu.copy_data_from_active", "Copy From Active", "COPYDOWN"),
        ("abu.operation_custom", "Custom Operation(s)", "MODIFIER"),
    ]
