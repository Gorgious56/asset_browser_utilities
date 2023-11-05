from pathlib import Path

import bpy
from bpy.types import PropertyGroup
from bpy.props import StringProperty, CollectionProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.library.prop import LibraryExportSettings
from asset_browser_utilities.core.library.tool import (
    get_directory_name,
    get_blend_data_name,
)
from asset_browser_utilities.core.file.path import open_file_if_different_from_current
from asset_browser_utilities.core.filter.container import get_all_assets_in_file

from asset_browser_utilities.module.library.tool import get_asset_uuid


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

    def populate(self):
        self.assets.clear()
        library_settings = get_from_cache(LibraryExportSettings)
        library_path = Path(library_settings.library_user_path)
        blend_files = [fp for fp in library_path.glob("**/*.blend") if fp.is_file()]
        print(f"Checking the content of library '{library_path}' :")
        origin_file = bpy.data.filepath
        for blend_file in blend_files:
            open_file_if_different_from_current(blend_file)
            for asset in get_all_assets_in_file():
                new_asset_dummy = self.assets.add()
                new_asset_dummy.init(
                    blend_file,
                    get_directory_name(asset),
                    asset.name,
                    get_blend_data_name(asset),
                    get_asset_uuid(asset),
                )
        open_file_if_different_from_current(origin_file)

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

    def by_filepath(self, filepath):
        yield from self.by_attribute("filepath", filepath)

    def how_many_assets_in_filepath(self, filepath):
        return len(list(self.by_filepath(filepath)))
