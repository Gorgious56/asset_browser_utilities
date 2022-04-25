from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType


class ABU_MT_tags(Menu):
    bl_label = "Tags"

    def draw(self, context):
        layout = self.layout
        library_source_from_context = LibraryType.get_library_type_from_context(context)
        add_tags_smart_op = layout.operator("asset.tags_add_smart", text="Add Smart", icon="OUTLINER_OB_LIGHT")
        add_tags_smart_op.library_settings.source = library_source_from_context
        add_tags_op = layout.operator("asset.batch_add_tags", text="Add", icon="ADD")
        add_tags_op.library_settings.source = library_source_from_context
        remove_tags_op = layout.operator("asset.batch_remove_tags", text="Remove", icon="REMOVE")
        remove_tags_op.library_settings.source = library_source_from_context
