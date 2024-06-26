from pathlib import Path
from uuid import uuid4
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.module.asset.tool import all_assets
import bpy
from asset_browser_utilities.module.catalog.prop import CatalogExportSettings
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType
from asset_browser_utilities.core.file.path import read_lines_sequentially


def all_catalogs():
    return CatalogsHelper().get_catalogs(None, None)


class CatalogsHelper:
    CATALOGS_FILENAME = "blender_assets.cats.txt"
    # https://blender.stackexchange.com/questions/216230/is-there-a-workaround-for-the-known-bug-in-dynamic-enumproperty
    CATALOGS_ENUM_HANDLE = {}

    def __init__(self):
        self.catalog_filepath = self.get_catalog_filepath()

    @classmethod
    def catalog_info_from_line(cls, catalog_line):
        return catalog_line.split(":")

    def get_catalog_filepath(self):
        context = bpy.context
        library_settings = get_from_cache(LibraryExportSettings)
        library_source = library_settings.source
        if library_source == LibraryType.FileCurrent.value:
            root_folder = Path(bpy.data.filepath).parent
        elif library_source in (LibraryType.FileExternal.value, LibraryType.FolderExternal.value):
            if context.area is None or context.area.type != "FILE_BROWSER":
                root_folder = Path(get_from_cache(CatalogExportSettings).path)
            else:
                file_browser_directory = context.area.spaces.active.params.directory  # Byte string
                root_folder = Path(file_browser_directory.decode("UTF-8"))
                if root_folder and str(root_folder) != ".":
                    get_from_cache(CatalogExportSettings).path = str(root_folder)
                else:
                    root_folder = Path(get_from_cache(CatalogExportSettings).path)
        elif library_source == LibraryType.UserLibrary.value:
            root_folder = Path(library_settings.library_user_path)
            catalog_filepath = root_folder / self.CATALOGS_FILENAME
            if not catalog_filepath.exists():
                self.create_catalog_file(catalog_filepath)
            return catalog_filepath
        else:
            raise Exception("The Library source is not correct")
        catalog_filepath = root_folder / self.CATALOGS_FILENAME
        while not catalog_filepath.exists():
            if catalog_filepath.parent == catalog_filepath.parent.parent:  # Root of the disk
                return None
            catalog_filepath = catalog_filepath.parent.parent / self.CATALOGS_FILENAME
        return catalog_filepath

    @property
    def has_catalogs(self):
        return self.catalog_filepath is not None and Path(self.catalog_filepath).exists()

    def create_catalog_file(self, filepath=None):
        if filepath is None:
            filepath = self.catalog_filepath
        with open(filepath, "w") as catalog_file:
            catalog_file.write("# This is an Asset Catalog Definition file for Blender.\n")
            catalog_file.write("#\n")
            catalog_file.write("# Empty lines and lines starting with `#` will be ignored.\n")
            catalog_file.write("# The first non-ignored line should be the version indicator.\n")
            catalog_file.write('# Other lines are of the format "UUID:catalog/path/for/assets:simple catalog name"\n')
            catalog_file.write("\n")
            catalog_file.write("VERSION 1\n")
            catalog_file.write("\n")

        Logger.display(f"Created catalog definition file at {filepath}")

    def add_catalog_to_catalog_file(self, catalog_uuid, catalog_tree, catalog_name):
        with open(self.catalog_filepath, "a") as catalog_file:
            catalog_file.write(f"{str(catalog_uuid)}:{str(catalog_tree)}:{str(catalog_name)}")

    def ensure_catalog_exists(self, catalog_uuid, catalog_tree, catalog_name):
        if not self.has_catalogs:
            self.create_catalog_file()
        if not self.is_catalog_in_catalog_file(catalog_uuid):
            self.add_catalog_to_catalog_file(catalog_uuid, catalog_tree, catalog_name)

    def ensure_or_create_catalog_definition(self, tree):
        if not self.has_catalogs:
            self.create_catalog_file()
        catalog_definition_lines_existing = list(self.iterate_over_catalogs())
        uuids_existing = [line.split(":")[0] for line in catalog_definition_lines_existing]
        catalog_trees_existing = [line.split(":")[1] for line in catalog_definition_lines_existing]
        with open(self.catalog_filepath, "a") as catalog_file:
            tree = str(tree)
            tree = tree.replace("\\", "/")
            if tree in catalog_trees_existing:
                uuid = uuids_existing[catalog_trees_existing.index(tree)]
            else:
                uuid = str(uuid4())
                catalog_name = tree.replace("/", "-")
                catalog_line = f"{uuid}:{tree}:{catalog_name}"
                catalog_file.write(catalog_line)
                catalog_file.write("\n")
                Logger.display(f"Created catalog definition {catalog_line} in {self.catalog_filepath}")
        return uuid

    def is_catalog_in_catalog_file(self, uuid):
        return self.catalog_info_from_uuid(uuid) is not None

    def catalog_info_from_uuid(self, uuid):
        for line in self.iterate_over_catalogs():
            this_uuid, tree, name = self.catalog_info_from_line(line)
            if this_uuid == uuid:
                return this_uuid, tree, name

    def iterate_over_catalogs(self):
        for line in read_lines_sequentially(self.catalog_filepath):
            if line.startswith(("#", "VERSION", "\n")):
                continue
            yield line.split("\n")[0]

    def catalog_line_from_uuid(self, uuid):
        for line in self.iterate_over_catalogs():
            this_uuid, _, _ = self.catalog_info_from_line(line)
            if this_uuid == uuid:
                return line

    def remove_catalog_by_uuid(self, uuid):
        lines = list(read_lines_sequentially(self.catalog_filepath))
        with open(self.catalog_filepath, "w") as catalog_file:
            for line in lines:
                if line.startswith(str(uuid)):
                    continue
                catalog_file.write(line)

    @staticmethod
    def get_catalogs(filter_catalog=None, context=None):  # Keep both arguments even if not used. It's a callback !
        helper = CatalogsHelper()
        CatalogsHelper.CATALOGS_ENUM_HANDLE[helper.catalog_filepath] = []

        if helper.has_catalogs:
            for line in helper.iterate_over_catalogs():
                uuid, tree, name = helper.catalog_info_from_line(line)
                CatalogsHelper.CATALOGS_ENUM_HANDLE[helper.catalog_filepath].append((uuid, tree, name))
        else:
            CatalogsHelper.CATALOGS_ENUM_HANDLE[helper.catalog_filepath] = [("",) * 3]
        return CatalogsHelper.CATALOGS_ENUM_HANDLE[helper.catalog_filepath]

    @staticmethod
    def get_catalogs_from_assets_in_current_file(filter_catalog=None, context=None) -> list[str]:
        catalogs_from_assets_in_current_file = set()
        for asset in all_assets():
            if not asset.catalog_simple_name:
                continue
            catalogs_from_assets_in_current_file.add((asset.catalog_id, asset.catalog_simple_name))
        return [(uuid, name, "") for (uuid, name) in catalogs_from_assets_in_current_file] or [("None",) * 3]
