import bpy
from bpy.types import PropertyGroup
from bpy.props import EnumProperty, StringProperty, BoolProperty

from asset_browser_utilities.helper.path import read_lines_sequentially, get_catalog_file, has_catalogs


def get_catalogs(self, context):
    catalogs = []
    for line in read_lines_sequentially(get_catalog_file(bpy.data.filepath)):
        if line.startswith(("#", "VERSION", "\n")):
            continue
        uuid, tree, name = line.split("\n")[0].split(":")
        catalogs.append((uuid, name, tree))
    return catalogs


class FilterCatalog(PropertyGroup):
    active: BoolProperty(default=False, name="Filter By Catalog")
    catalog: EnumProperty(items=get_catalogs, name="Catalog")

    def draw(self, layout):
        if not has_catalogs(bpy.data.filepath):
            return
        box = layout.box()
        box.prop(self, "active", icon="FILTER")
        if self.active:
            box.prop(self, "catalog")
