from bpy.types import PropertyGroup
from bpy.props import EnumProperty, BoolProperty

from asset_browser_utilities.catalog.tool import CatalogsHelper


class FilterCatalog(PropertyGroup):
    active: BoolProperty(default=False, name="Filter By Catalog")
    catalog: EnumProperty(items=CatalogsHelper.get_catalogs, name="Catalog")

    def draw(self, layout, context):
        helper = CatalogsHelper(context)
        if not helper.has_catalogs:
            return
        box = layout.box()
        box.prop(self, "active", icon="FILTER")
        if self.active:
            box.prop(self, "catalog")
