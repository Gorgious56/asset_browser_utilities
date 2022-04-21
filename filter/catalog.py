from bpy.types import PropertyGroup
from bpy.props import EnumProperty, BoolProperty

from asset_browser_utilities.catalog.tool import CatalogsHelper


class FilterCatalog(PropertyGroup):
    active: BoolProperty(default=False, name="Filter By Catalog")
    catalog: EnumProperty(items=CatalogsHelper.get_catalogs, name="Catalog")

    def draw(self, layout, context):
        box = layout.box()
        box.prop(self, "active", icon="FILTER")
        if self.active:
            helper = CatalogsHelper(context)
            if helper.has_catalogs:
                box.prop(self, "catalog")
            else:
                box.label(text="No catalog in root folder", icon="INFO")
