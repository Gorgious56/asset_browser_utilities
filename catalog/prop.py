import bpy
from bpy.types import PropertyGroup
from bpy.props import EnumProperty, StringProperty, BoolProperty

from asset_browser_utilities.file.path import has_catalogs
from asset_browser_utilities.catalog.helper import get_catalogs


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
