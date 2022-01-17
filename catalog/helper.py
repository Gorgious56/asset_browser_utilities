import os.path
from pathlib import Path
import bpy
from asset_browser_utilities.file.path import read_lines_sequentially


def get_catalog_filepath(blend_filepath):
    folder = Path(blend_filepath).parent
    return folder / "blender_assets.cats.txt"


def has_catalogs(blend_filepath):
    return os.path.exists(get_catalog_filepath(blend_filepath))


def create_catalog_file(catalog_filepath):
    with open(catalog_filepath, "w") as catalog_file:
        catalog_file.write("# This is an Asset Catalog Definition file for Blender.")
        catalog_file.write("#")
        catalog_file.write("# Empty lines and lines starting with `#` will be ignored.")
        catalog_file.write("# The first non-ignored line should be the version indicator.")
        catalog_file.write('# Other lines are of the format "UUID:catalog/path/for/assets:simple catalog name"')
        catalog_file.write("")
        catalog_file.write("VERSION 1")
        catalog_file.write("")


def ensure_catalog_exists(catalog_uuid, catalog_tree, catalog_name, blend_filepath=None):
    if blend_filepath is None:
        blend_filepath = bpy.data.filepath
    catalog_filepath = get_catalog_filepath(blend_filepath)
    if not has_catalogs(blend_filepath):
        create_catalog_file(catalog_filepath)
    if not is_catalog_in_catalog_file(catalog_uuid, blend_filepath):
        with open(catalog_filepath, "a") as catalog_file:
            catalog_file.write(f"{str(catalog_uuid)}:{str(catalog_tree)}:{str(catalog_name)}")


def iterate_over_catalogs(blend_filepath=None):
    if blend_filepath is None:
        blend_filepath = bpy.data.filepath
    for line in read_lines_sequentially(get_catalog_filepath(blend_filepath)):
        if line.startswith(("#", "VERSION", "\n")):
            continue
        yield line.split("\n")[0]


def is_catalog_in_catalog_file(uuid, blend_filepath=None):
    return get_catalog_info_from_uuid is not None


def get_catalog_info_from_line(catalog_line):
    return catalog_line.split(":")


def get_catalog_info_from_uuid(uuid, blend_filepath=None):
    if blend_filepath is None:
        blend_filepath = bpy.data.filepath
    for line in iterate_over_catalogs(blend_filepath):
        this_uuid, tree, name = get_catalog_info_from_line(line)
        if this_uuid == uuid:
            return this_uuid, tree, name


def get_catalog_line_from_uuid(uuid, blend_filepath=None):
    if blend_filepath is None:
        blend_filepath = bpy.data.filepath
    for line in iterate_over_catalogs(blend_filepath):
        this_uuid, _, _ = get_catalog_info_from_line(line)
        if this_uuid == uuid:
            return line


def get_catalogs(self, context):
    catalogs = []
    for line in iterate_over_catalogs():
        uuid, tree, name = get_catalog_info_from_line(line)
        catalogs.append((uuid, tree, name))
    return catalogs
