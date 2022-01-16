import os.path
import bpy
from asset_browser_utilities.file.path import read_lines_sequentially, get_catalog_file


def has_catalogs(filepath):
    return os.path.exists(get_catalog_file(filepath))


def get_catalogs(self, context):
    catalogs = []
    for line in read_lines_sequentially(get_catalog_file(bpy.data.filepath)):
        if line.startswith(("#", "VERSION", "\n")):
            continue
        uuid, tree, name = line.split("\n")[0].split(":")
        catalogs.append((uuid, name, tree))
    return catalogs
