from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType


class ABU_MT_custom_properties(Menu):
    bl_label = "Custom Properties"

    def draw(self, context):
        layout = self.layout
        library_source_from_context = LibraryType.get_library_type_from_context(context)
        add_tags_smart_op = layout.operator("asset.batch_set_custom_property", text="Set", icon="ADD")
        add_tags_smart_op.library_settings.source = library_source_from_context
