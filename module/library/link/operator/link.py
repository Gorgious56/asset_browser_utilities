import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.filter.container import get_all_assets_in_file
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.core.file.path import open_file_if_different_from_current
from asset_browser_utilities.core.log.logger import Logger

from asset_browser_utilities.module.library.link.prop import AssetLibraryDummy
from asset_browser_utilities.module.library.link.tool import link_from_asset_dummy
from asset_browser_utilities.module.library.tool import ensure_asset_uuid


class AssetLinkBatchExecute(BatchExecute):
    def __init__(self, file_extension="blend"):
        library_dummy = get_current_operator_properties().library
        library_dummy.populate()
        self.root_assets_dummies = [library_dummy.assets[i.value] for i in library_dummy.unique_assets_indices]
        self.root_assets_dummies_uuids = [root_asset.uuid for root_asset in self.root_assets_dummies]
        super().__init__()

    def open_next_file(self):
        self.file = self.files.pop(0)
        library_dummy = get_current_operator_properties().library
        asset_dummies_in_file = list(library_dummy.by_filepath(str(self.file)))
        if len(asset_dummies_in_file) > 1:
            # We only want to link if there is more than one asset in the file
            for asset_dummy_in_file in asset_dummies_in_file:
                if asset_dummy_in_file not in self.root_assets_dummies:
                    open_file_if_different_from_current(str(self.file))
                    return True
        Logger.display(f"{str(self.file)} should NOT be linked")
        return False

    def execute_one_file_and_the_next_when_finished(self):
        library_dummy = get_current_operator_properties().library
        should_save = False
        if library_dummy.how_many_assets_in_filepath(bpy.data.filepath) > 1:
            # We only want to link if there is more than one asset in the file
            all_assets_in_file = list(get_all_assets_in_file())
            for asset_in_file in all_assets_in_file:
                asset_in_file_dummy = next(
                    library_dummy.intersect(
                        filepath=bpy.data.filepath,
                        uuid=ensure_asset_uuid(asset_in_file),
                    ),
                    None,
                )
                if asset_in_file_dummy is None or asset_in_file_dummy in self.root_assets_dummies:
                    continue
                root_asset_dummy = self.root_assets_dummies[
                    self.root_assets_dummies_uuids.index(asset_in_file_dummy.uuid)
                ]
                link_from_asset_dummy(root_asset_dummy, asset_in_file, purge=True)
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