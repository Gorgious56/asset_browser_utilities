from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty, CollectionProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator

from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType
from asset_browser_utilities.core.library.tool import (
    get_directory_name,
    link_asset,
    get_blend_data_name_from_directory,
)

from asset_browser_utilities.core.filter.container import get_all_assets_in_file


import bpy
from pathlib import Path


class Asset(PropertyGroup):
    name: StringProperty()
    directory: StringProperty()
    filepath: StringProperty()
    blenddata_name: StringProperty()

    def init(self, blend_filepath, directory, name, blenddata_name) -> None:
        self.name = name
        self.directory = directory
        self.filepath = str(blend_filepath)
        self.blenddata_name = blenddata_name


class AssetLibrary(PropertyGroup):
    assets: CollectionProperty(type=Asset)

    def by_attribute(self, attr, value):
        for asset in self.assets:
            if getattr(asset, attr) == value:
                yield asset

    def by_directory(self, directory: str):
        yield from self.by_attribute("directory", directory.lower())

    def by_name(self, name):
        yield from self.by_attribute("name", name)

    def by_directory_and_name(self, directory, name):
        assets = set(self.by_name(name))
        assets.intersection_update(self.by_directory(directory))
        yield from assets

    def by_filepath(self, filepath):
        yield from self.by_attribute("filepath", filepath)


class AssetLinkBatchExecute(BatchExecute):
    def __init__(self, file_extension="blend"):
        library_settings = get_from_cache(LibraryExportSettings)
        library_path = Path(library_settings.library_user_path)
        blend_files = [fp for fp in library_path.glob("**/*.blend") if fp.is_file()]
        print(f"Checking the content of library '{library_path}' :")
        asset_library_dummy = get_current_operator_properties().library
        for blend_file in blend_files:
            directory = str(blend_file.parent.name)
            blenddata_name = get_blend_data_name_from_directory(directory)
            with bpy.data.libraries.load(str(blend_file), assets_only=True) as (file_contents, _):
                blend_file_assets = getattr(file_contents, blenddata_name)
                for blend_file_asset in blend_file_assets:
                    new_asset_dummy = asset_library_dummy.assets.add()
                    new_asset_dummy.init(blend_file, directory, blend_file_asset, blenddata_name)
        super().__init__(file_extension)

    def execute_one_file_and_the_next_when_finished(self):
        library_dummy = get_current_operator_properties().library
        asset_dummies = library_dummy.by_filepath(bpy.data.filepath)
        assets_to_keep = []
        for asset_dummy in asset_dummies:
            assets_to_keep.append(getattr(bpy.data, asset_dummy.blenddata_name)[asset_dummy.name])
        all_assets_in_file = list(get_all_assets_in_file())
        assets_to_discard = set(all_assets_in_file) - set(assets_to_keep)
        for asset_to_discard in assets_to_discard:
            corresponding_asset_dummy = next(
                (library_dummy.by_directory_and_name(get_directory_name(asset_to_discard), asset_to_discard.name)),
                None,
            )
            if corresponding_asset_dummy:
                filepath, directory, name = (
                    corresponding_asset_dummy.filepath,
                    corresponding_asset_dummy.directory,
                    corresponding_asset_dummy.name,
                )
                linked_asset = link_asset(filepath, directory, name)
                Logger.display(f"Linked Asset '{directory}/{name}' from {filepath}'")
                asset_to_discard.user_remap(linked_asset)
                asset_to_discard.asset_clear()
                asset_to_discard.use_fake_user = False
                Logger.display(f"Remapped users of old asset `{repr(asset_to_discard)}' to {repr(linked_asset)}'")
        self.save_file()
        self.execute_next_file()


class AssetLinkOperatorProperties(PropertyGroup):
    library: PointerProperty(type=AssetLibrary)

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
