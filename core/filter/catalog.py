from bpy.types import PropertyGroup
from bpy.props import EnumProperty, BoolProperty, StringProperty

from asset_browser_utilities.module.catalog.tool import CatalogsHelper


def update_uuid(self, context):
    self.catalog_uuid = self.catalog
    self.catalog_filepath = str(CatalogsHelper().catalog_filepath)
    # TODO update root filepath


class FilterCatalog(PropertyGroup):
    active: BoolProperty(default=False, name="Filter By Catalog")
    allow: BoolProperty(default=False)
    from_current_file: BoolProperty(default=False)
    catalog_from_definition: EnumProperty(items=CatalogsHelper.get_catalogs, name="Catalog", update=update_uuid)
    catalog_from_current_file: EnumProperty(
        items=CatalogsHelper.get_catalogs_from_assets_in_current_file, name="Catalog", update=update_uuid
    )
    catalog_uuid: StringProperty()
    catalog_filepath: StringProperty(name="Path")

    @property
    def catalog(self):
        return getattr(self, self.catalog_attribute)

    @catalog.setter
    def catalog(self, value):
        setattr(self, self.catalog_attribute, value)

    @property
    def catalog_attribute(self):
        return "catalog_from_current_file" if self.from_current_file else "catalog_from_definition"

    def draw_filepath(self, layout):
        layout.prop(self, "catalog_filepath", icon="FILEBROWSER")

    def draw(self, layout, context, draw_filter=True, draw_filepath=True):
        if draw_filter:
            layout = layout.box()
            layout.prop(self, "active", icon="FILTER")
        if self.active:
            if self.from_current_file:
                layout.prop(self, "catalog_from_current_file")
            else:
                helper = CatalogsHelper()
                if helper.has_catalogs:
                    layout.prop(self, "catalog_from_definition", icon="ASSET_MANAGER")
                else:
                    layout.label(text="No catalog in root folder", icon="INFO")
                if draw_filepath:
                    self.draw_filepath(layout)
