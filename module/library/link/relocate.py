from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty, CollectionProperty
from asset_browser_utilities.core.cache.tool import get_current_operator_properties

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator

from asset_browser_utilities.module.library.link.prop import AssetLibrary
from asset_browser_utilities.module.library.link.tool import link_from_asset_dummy
from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType
from asset_browser_utilities.core.library.tool import (
    get_directory_name,
    link_asset,
    get_blend_data_name_from_directory,
)

from asset_browser_utilities.core.filter.container import get_all_assets_in_file


import bpy
from pathlib import Path


class AssetLinkRelocateBatchExecute(BatchExecute):
    def __init__(self, file_extension="blend"):
        get_current_operator_properties().library.populate()
        super().__init__(file_extension)

    def execute_one_file_and_the_next_when_finished(self):
        library_dummy = get_current_operator_properties().library
        for blend_data_library in bpy.data.libraries:
            if blend_data_library.is_missing:
                for asset in blend_data_library.users_id:
                    directory = get_directory_name(asset)
                    name = asset.name
                    corresponding_asset_dummy = next((library_dummy.by_directory_and_name(directory, name)), None)
                    if corresponding_asset_dummy:
                        link_from_asset_dummy(corresponding_asset_dummy, asset)
        self.save_file()
        self.execute_next_file()


class AssetLinkRelocateOperatorProperties(PropertyGroup):
    library: PointerProperty(type=AssetLibrary)

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
