import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.filter.container import get_all_assets_in_file
from asset_browser_utilities.core.file.path import open_file_if_different_from_current
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps
from asset_browser_utilities.core.log.logger import Logger

from asset_browser_utilities.module.library.link.prop import AssetLibraryDummy
from asset_browser_utilities.module.library.link.tool import replace_with_asset_dummy, link_from_asset_dummy
from asset_browser_utilities.module.library.tool import ensure_asset_uuid


class AssetUpdateOperatorProperties(PropertyGroup, BaseOperatorProps):
    library: PointerProperty(type=AssetLibraryDummy)
    link_back: BoolProperty(name="Link Back")

    def draw(self, layout, context=None):
        layout.prop(self, "link_back", icon="LINKED")
        return

    def init(self):
        self.library.populate()
        self.root_assets_dummies = [self.library.assets[i.value] for i in self.library.unique_assets_indices]

    def run_in_file(self, attributes=None):
        should_save = False
        all_assets_in_file = list(get_all_assets_in_file())
        for asset_in_file in all_assets_in_file:
            asset_in_file_dummy = next(
                self.library.intersect(
                    filepath=bpy.data.filepath,
                    uuid=ensure_asset_uuid(asset_in_file),
                ),
                None,
            )
            if asset_in_file_dummy in self.root_assets_dummies:
                other_asset_dummy = next(
                    (d for d in self.library.by_uuid(asset_in_file_dummy.uuid) if d != asset_in_file_dummy), None
                )
                if other_asset_dummy:
                    Logger.display(
                        f"Updating root asset {repr(asset_in_file)} with {other_asset_dummy.filepath}/{other_asset_dummy.directory}/{other_asset_dummy.name}"
                    )
                    replace_with_asset_dummy(other_asset_dummy, asset_in_file, purge=True)
                    asset_in_file_dummy.name = other_asset_dummy.name
                    if get_current_operator_properties().link_back:
                        self.save_file()
                        open_file_if_different_from_current(other_asset_dummy.filepath)
                        for asset in list(get_all_assets_in_file()):
                            if (ensure_asset_uuid(asset)) == other_asset_dummy.uuid:
                                link_from_asset_dummy(asset_in_file_dummy, asset)
                                self.save_file(other_asset_dummy.filepath)
                                break
                        open_file_if_different_from_current(asset_in_file_dummy.filepath)
                    else:
                        should_save = True
        return should_save


class ABU_OT_asset_update(Operator, BatchFolderOperator):
    ui_library = LibraryType.UserLibrary.value
    bl_idname = "abu.asset_update"
    bl_label = "Batch Update Assets"
    bl_description = "Batch Update Assets to an asset library"

    operator_settings: PointerProperty(type=AssetUpdateOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)

    def filter_files(self, files):
        files = super().filter_files(files)
        files_to_operate_on = []
        for file in files:
            library_dummy = get_current_operator_properties().library
            asset_dummies_in_file = library_dummy.by_filepath(str(file))
            for asset_dummy_in_file in asset_dummies_in_file:
                if asset_dummy_in_file in get_current_operator_properties().root_assets_dummies:
                    other_asset_dummy = next(
                        (d for d in library_dummy.by_uuid(asset_dummy_in_file.uuid) if d != asset_dummy_in_file), None
                    )
                    if other_asset_dummy:
                        files_to_operate_on.append(file)
        return files_to_operate_on
