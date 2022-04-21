from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType


class ABU_MT_catalogs(Menu):
    bl_label = "Catalogs"

    def draw(self, context):
        layout = self.layout
        library_type = LibraryType.get_library_type_from_context(context)
        ops = []
        ops.append(layout.operator("asset.batch_move_to_catalog", text="Move To Catalog", icon="ADD"))
        ops.append(layout.operator("asset.batch_remove_from_catalog", text="Remove From Catalog", icon="REMOVE"))
        ops.append(
            layout.operator("asset.batch_move_from_cat_a_to_cat_b", text="Move From A to B", icon="FOLDER_REDIRECT")
        )
        for op in ops:
            op.library_settings.library_type = library_type
