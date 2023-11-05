from pathlib import Path

import bpy
from bpy.types import PropertyGroup
from bpy.props import StringProperty, CollectionProperty

from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.library.prop import LibraryExportSettings
from asset_browser_utilities.core.library.tool import get_blend_data_name_from_directory


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
    def populate(self):
        library_settings = get_from_cache(LibraryExportSettings)
        library_path = Path(library_settings.library_user_path)
        blend_files = [fp for fp in library_path.glob("**/*.blend") if fp.is_file()]
        print(f"Checking the content of library '{library_path}' :")
        for blend_file in blend_files:
            directory = str(blend_file.parent.name)
            blenddata_name = get_blend_data_name_from_directory(directory)
            with bpy.data.libraries.load(str(blend_file), assets_only=True) as (file_contents, _):
                blend_file_asset_names = getattr(file_contents, blenddata_name)
                for blend_file_asset_name in blend_file_asset_names:
                    new_asset_dummy = self.assets.add()
                    new_asset_dummy.init(blend_file, directory, blend_file_asset_name, blenddata_name)

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

    def by_blend_data_name_and_name(self, blenddata_name, name):
        assets = set(self.by_name(name))
        assets.intersection_update(self.by_attribute("blenddata_name", blenddata_name))
        yield from assets

    def by_filepath(self, filepath):
        yield from self.by_attribute("filepath", filepath)
