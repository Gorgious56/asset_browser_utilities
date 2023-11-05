from pathlib import Path
from collections import defaultdict

import bpy
from bpy.types import PropertyGroup
from bpy.props import StringProperty, CollectionProperty, PointerProperty

from asset_browser_utilities.core.prop import IntPropertyCollection, AnyID
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.library.prop import LibraryExportSettings
from asset_browser_utilities.core.library.tool import (
    get_directory_name,
    get_blend_data_name,
)
from asset_browser_utilities.core.file.path import open_file_if_different_from_current
from asset_browser_utilities.core.filter.container import get_all_assets_in_file

from asset_browser_utilities.module.library.tool import ensure_asset_uuid


class AssetDummyWithPointer(PropertyGroup):
    asset: PointerProperty(type=AnyID)
    name: StringProperty()
    directory: StringProperty()
    filepath: StringProperty()
    blenddata_name: StringProperty()
    uuid: StringProperty()


class AssetLibraryDummyWithPointer(PropertyGroup):
    assets: CollectionProperty(type=AssetDummyWithPointer)


class AssetDummy(PropertyGroup):
    name: StringProperty()
    directory: StringProperty()
    filepath: StringProperty()
    blenddata_name: StringProperty()
    uuid: StringProperty()

    def init(self, blend_filepath, directory, name, blenddata_name, uuid) -> None:
        self.name = name
        self.directory = directory
        self.filepath = str(blend_filepath)
        self.blenddata_name = blenddata_name
        self.uuid = uuid

    def __str__(self):
        return f"{self.filepath}, {self.name}, {self.uuid}"


class AssetLibraryDummy(PropertyGroup):
    assets: CollectionProperty(type=AssetDummy)
    unique_assets_indices: CollectionProperty(type=IntPropertyCollection)

    def init_assets(self):
        library_settings = get_from_cache(LibraryExportSettings)
        library_path = Path(library_settings.library_user_path)
        blend_files = [fp for fp in library_path.glob("**/*.blend") if fp.is_file()]
        Logger.display(f"Checking the content of library '{library_path}' :")
        for i, blend_file in enumerate(blend_files):
            Logger.display(f"Fetching data... {len(blend_files) - i} files left")
            open_file_if_different_from_current(blend_file)
            for asset in get_all_assets_in_file():
                new_asset_dummy = self.assets.add()
                new_asset_dummy.init(
                    blend_file,
                    get_directory_name(asset),
                    asset.name,
                    get_blend_data_name(asset),
                    ensure_asset_uuid(asset),
                )

    def init_unique_assets(self):
        unique_uuids = []
        filepath_to_assets_map = self.filepath_to_assets_map()
        while True:
            for filepath, assets in filepath_to_assets_map.items():
                if len(assets) == 0:
                    del filepath_to_assets_map[filepath]
                    break
                elif len(assets) == 1:
                    self.unique_assets_indices.add().value = self.asset_index(assets[0])
                    unique_uuids.append(assets[0].uuid)
                    del filepath_to_assets_map[filepath]
                    break
                assets_before = len(assets)
                filepath_to_assets_map[filepath] = [a for a in assets if a.uuid not in unique_uuids]
                if assets_before != len(filepath_to_assets_map[filepath]):
                    break
            else:
                for filepath, assets in filepath_to_assets_map.items():
                    for asset in assets:
                        self.unique_assets_indices.add().value = self.asset_index(asset)
                break

    def populate(self):
        self.assets.clear()
        self.unique_assets_indices.clear()
        origin_file = bpy.data.filepath if bpy.data.is_saved else None
        self.init_assets()
        if origin_file:
            open_file_if_different_from_current(origin_file)
        self.init_unique_assets()

    def asset_index(self, asset_search):
        for i, asset in enumerate(self.assets):
            if asset == asset_search:
                return i
        return -1

    def by_attribute(self, attr, value):
        for asset in self.assets:
            if getattr(asset, attr) == value:
                yield asset

    def by_uuid(self, uuid):
        if not uuid:
            return None
        yield from self.by_attribute("uuid", uuid)

    def by_directory(self, directory: str):
        yield from self.by_attribute("directory", directory.lower())

    def by_name(self, name):
        yield from self.by_attribute("name", name)

    def by_directory_and_name(self, directory, name):
        assets = set(self.by_name(name))
        assets.intersection_update(self.by_directory(directory))
        yield from assets

    def intersect(self, **args):
        assets = set(self.assets[:])
        for attr_name, attr_value in args.items():
            assets.intersection_update(self.by_attribute(attr_name, attr_value))
        yield from assets

    def by_blend_data_name_and_name(self, blenddata_name, name):
        assets = set(self.by_name(name))
        assets.intersection_update(self.by_attribute("blenddata_name", blenddata_name))
        yield from assets

    def filepath_to_assets_map(self):
        filepath_to_assets_map = defaultdict(list)
        for asset in self.assets:
            filepath_to_assets_map[asset.filepath].append(asset)
        return filepath_to_assets_map

    def by_filepath(self, filepath=None):
        yield from self.by_attribute("filepath", filepath)

    def how_many_assets_in_filepath(self, filepath):
        return len(list(self.by_filepath(filepath)))


def register():
    bpy.types.Library.abu_asset_library_dummy = PointerProperty(type=AssetLibraryDummyWithPointer)
