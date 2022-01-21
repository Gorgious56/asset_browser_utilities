from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType


class ABU_MT_assets(Menu):
    bl_label = "Assets"

    def draw(self, context):
        layout = self.layout

        library_type = LibraryType.get(context)
        ops = []
        ops.append(layout.operator("asset.batch_mark", text="Mark", icon="SHADERFX"))
        ops.append(layout.operator("asset.batch_unmark", text="Unmark", icon="TRASH"))
        for op in ops:
            op.library_settings.library_type = library_type
        if library_type == LibraryType.FileCurrent.value:
            layout.operator("asset.batch_import", text="Import", icon="IMPORT")
            layout.operator("asset.batch_export", text="Export", icon="EXPORT")
