import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.core.filter.container import get_all_assets_in_file
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps
from asset_browser_utilities.core.log.logger import Logger

from asset_browser_utilities.module.library.link.prop import AssetLibraryDummy
from asset_browser_utilities.module.library.link.tool import link_from_asset_dummy
from asset_browser_utilities.module.library.tool import ensure_asset_uuid


class AssetLinkOperatorProperties(PropertyGroup, BaseOperatorProps):
    library: PointerProperty(type=AssetLibraryDummy)

    def draw(self, layout, context=None):
        return

    def init(self):
        self.library.populate()
        self.root_assets_dummies = [self.library.assets[i.value] for i in self.library.unique_assets_indices]
        self.root_assets_dummies_uuids = [root_asset.uuid for root_asset in self.root_assets_dummies]

    def run_in_file(self, attributes=None):
        if self.library.how_many_assets_in_filepath(bpy.data.filepath) > 1:
            # We only want to link if there is more than one asset in the file
            all_assets_in_file = list(get_all_assets_in_file())
            for asset_in_file in all_assets_in_file:
                asset_in_file_dummy = next(
                    self.library.intersect(
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


class ABU_OT_asset_link(Operator, BatchFolderOperator):
    ui_library = LibraryType.UserLibrary.value
    bl_idname = "abu.asset_link"
    bl_label = "Batch Link Assets"
    bl_description = "Batch link assets from an asset library"

    operator_settings: PointerProperty(type=AssetLinkOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)

    def filter_files(self, files):
        files = super().filter_files(files)
        files_that_should_be_linked = []
        for file in files:
            library_dummy = get_from_cache(AssetLinkOperatorProperties).library
            asset_dummies_in_file = list(library_dummy.by_filepath(str(file)))
            if len(asset_dummies_in_file) > 1:
                # We only want to link if there is more than one asset in the file
                for asset_dummy_in_file in asset_dummies_in_file:
                    if asset_dummy_in_file not in self.root_assets_dummies:
                        files_that_should_be_linked.append(file)
                        continue
        return files_that_should_be_linked
