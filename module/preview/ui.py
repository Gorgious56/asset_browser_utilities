from bpy.types import Menu
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.ui.menu.operators import ABUOperatorsMenu


class ABU_MT_previews(Menu, ABUOperatorsMenu):
    bl_label = "Previews"
    ops_cmd = [
        ("abu.preview_generate", "Generate", "FILE_REFRESH"),
        ("abu.preview_import", "Load From Disk", "IMPORT"),
        ("abu.preview_extract", "Extract to Disk", "EXPORT"),
    ]
