import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty, CollectionProperty

from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator

from asset_browser_utilities.module.library.link.prop import AssetLibraryDummy
from asset_browser_utilities.module.library.link.tool import link_from_asset_dummy


class AssetLinkRelocateBatchExecute(BatchExecute):
    def __init__(self, file_extension="blend"):
        get_current_operator_properties().library.populate()
        super().__init__()

    def execute_one_file_and_the_next_when_finished(self):
        library_dummy = get_current_operator_properties().library
        should_save = False
        for blend_data_library in bpy.data.libraries:
            if blend_data_library.is_missing:
                for asset_dummy in blend_data_library.abu_asset_library_dummy.assets:
                    corresponding_asset_dummy = next((library_dummy.by_uuid(asset_dummy.uuid)), None)
                    if corresponding_asset_dummy:
                        should_save = True
                        link_from_asset_dummy(corresponding_asset_dummy, asset_dummy.asset.get(), purge=True)
            for linked_asset in blend_data_library.users_id:
                if linked_asset.is_missing:
                    for linked_asset_dummy in blend_data_library.abu_asset_library_dummy.assets:
                        if linked_asset_dummy.asset.get() == linked_asset:
                            corresponding_asset_dummy = next((library_dummy.by_uuid(linked_asset_dummy.uuid)), None)
                            if corresponding_asset_dummy:
                                should_save = True
                                link_from_asset_dummy(corresponding_asset_dummy, linked_asset, purge=True)
                                break
        if should_save:
            self.save_file()
        self.execute_next_file()


class AssetLinkRelocateOperatorProperties(PropertyGroup):
    library: PointerProperty(type=AssetLibraryDummy)

    def draw(self, layout, context=None):
        return


class ABU_OT_asset_link_relocate(Operator, BatchFolderOperator):
    ui_library = LibraryType.UserLibrary.value
    bl_idname = "abu.asset_link_relocate"
    bl_label = "Batch Relocate Links"
    bl_description = "Batch relocate linked assets from an asset library"

    operator_settings: PointerProperty(type=AssetLinkRelocateOperatorProperties)
    logic_class = AssetLinkRelocateBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
