from bpy.types import Menu
from asset_browser_utilities.library.prop import LibraryType


class ABU_MT_custom_properties(Menu):
    bl_label = "Custom Properties"

    def draw(self, context):
        layout = self.layout
        library_source_from_context = LibraryType.get_library_type_from_context(context)
        op = layout.operator("asset.batch_set_custom_property", text="Set", icon="ADD")
        op.library_settings.source = library_source_from_context
        op = layout.operator("asset.batch_remove_custom_property", text="Remove", icon="REMOVE")
        op.library_settings.source = library_source_from_context
