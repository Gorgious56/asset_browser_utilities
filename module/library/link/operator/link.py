import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.filter.container import get_all_assets_in_file
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.library.tool import get_directory_name
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator

from asset_browser_utilities.module.library.link.prop import AssetLibraryDummy
from asset_browser_utilities.module.library.link.tool import link_from_asset_dummy
from asset_browser_utilities.module.library.tool import get_asset_uuid
from asset_browser_utilities.module.tag.tool import add_asset_tag_link_uuid_from_other_uuid_and_name


class AssetLinkBatchExecute(BatchExecute):
    def __init__(self, file_extension="blend"):
        get_current_operator_properties().library.populate()
        super().__init__(file_extension)

    def execute_one_file_and_the_next_when_finished(self):
        library_dummy = get_current_operator_properties().library
        should_save = False
        if library_dummy.how_many_assets_in_filepath(bpy.data.filepath) > 1:
            # We only want to link if there is more than one asset in the file
            all_assets_in_file = list(get_all_assets_in_file())

            for asset_in_file in all_assets_in_file:
                corresponding_asset_dummies = library_dummy.by_uuid(get_asset_uuid(asset_in_file))
                for corresponding_asset_dummy in corresponding_asset_dummies:
                    if corresponding_asset_dummy.filepath == bpy.data.filepath:
                        # We don't want to link from ourself
                        continue
                    elif library_dummy.how_many_assets_in_filepath(corresponding_asset_dummy.filepath) > 1:
                        # We only want to link from one-asset-per-file blends
                        continue
                    else:
                        all_assets_in_file.remove(asset_in_file)
                        link_from_asset_dummy(corresponding_asset_dummy, asset_in_file, purge=True)
                        for asset in all_assets_in_file:
                            add_asset_tag_link_uuid_from_other_uuid_and_name(
                                    asset,
                                    corresponding_asset_dummy.uuid,
                                    corresponding_asset_dummy.name,
                                )
                        should_save = True

        if should_save:
            self.save_file()
        self.execute_next_file()


class AssetLinkOperatorProperties(PropertyGroup):
    library: PointerProperty(type=AssetLibraryDummy)

    def draw(self, layout, context=None):
        return


class ABU_OT_asset_link(Operator, BatchFolderOperator):
    ui_library = LibraryType.UserLibrary.value
    bl_idname = "abu.asset_link"
    bl_label = "Batch Link Assets"
    bl_description = "Batch link assets from an asset library"

    operator_settings: PointerProperty(type=AssetLinkOperatorProperties)
    logic_class = AssetLinkBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
