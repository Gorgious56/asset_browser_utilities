from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType


class ABU_MT_assets(Menu):
    bl_label = "Assets"

    def draw(self, context):
        layout = self.layout

        library_source_from_context = LibraryType.get_library_type_from_context(context)
        ops = []
        ops.append(layout.operator("asset.batch_mark", text="Mark", icon="SHADERFX"))
        ops.append(layout.operator("asset.batch_unmark", text="Unmark", icon="TRASH"))
        ops.append(layout.operator("asset.batch_operate", text="Custom Operation", icon="MODIFIER"))
        if library_source_from_context == LibraryType.FileCurrent.value:
            layout.operator("asset.batch_export", text="Export", icon="EXPORT")
        else:
            ops.append(layout.operator("asset.batch_import", text="Import", icon="IMPORT"))
        for op in ops:
            op.library_settings.source = library_source_from_context
