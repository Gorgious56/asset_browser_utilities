from bpy.types import PropertyGroup
from bpy.props import EnumProperty, BoolProperty, StringProperty

from asset_browser_utilities.module.catalog.tool import CatalogsHelper


def update_uuid(self, context):
    self.catalog_uuid = self.catalog
    # TODO update root filepath


class FilterCatalog(PropertyGroup):
    allow: BoolProperty(default=False)
    active: BoolProperty(default=False, name="Filter By Catalog")
    catalog: EnumProperty(items=CatalogsHelper.get_catalogs, name="Catalog", update=update_uuid)
    catalog_uuid: StringProperty()
    catalog_filepath: StringProperty()

    def draw_filepath(self, layout):
        helper = CatalogsHelper()
        layout.label(icon="INFO", text="File : " + str(helper.catalog_filepath))

    def draw(self, layout, context):
        box = layout.box()
        box.prop(self, "active", icon="FILTER")
        if self.active:
            helper = CatalogsHelper()
            if helper.has_catalogs:
                box.prop(self, "catalog")
            else:
                box.label(text="No catalog in root folder", icon="INFO")
            self.draw_filepath(box)
