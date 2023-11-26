from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.core.log.logger import Logger

from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps
from asset_browser_utilities.core.filter.catalog import FilterCatalog
from asset_browser_utilities.module.catalog.tool import CatalogsHelper


class CatalogRemoveFromOperatorProperties(PropertyGroup, BaseOperatorProps):
    filter: BoolProperty(default=True, description="")
    catalog: PointerProperty(type=FilterCatalog)

    def init(self, from_current_file=False):
        self.catalog.active = True
        self.catalog.from_current_file = from_current_file
        self.catalog.catalog_filepath = str(CatalogsHelper().catalog_filepath)

    def draw(self, layout, context=None):
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Remove Assets From This Catalog" if self.filter else "Remove Assets From All Catalogs")
        row.prop(self, "filter", icon="FILTER", text="")
        if self.filter:
            self.catalog.draw(box, context, draw_filter=False)

    def run_in_file(self, attributes=None):
        helper = CatalogsHelper()
        if self.filter:
            uuid, _, name = helper.catalog_info_from_uuid(self.catalog.catalog)
            for asset in self.get_assets():
                if asset.asset_data.catalog_id == uuid:
                    asset.asset_data.catalog_id = ""
                    Logger.display(f"{repr(asset)} unassigned from catalog '{name}'")
        else:
            for asset in self.get_assets():
                asset.asset_data.catalog_id = ""
                Logger.display(f"{repr(asset)} unassigned from its catalog")


class ABU_OT_catalog_remove_from(Operator, BatchFolderOperator):
    bl_idname = "abu.catalog_remove_from"
    bl_label = "Batch Remove From Catalog"

    operator_settings: PointerProperty(type=CatalogRemoveFromOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(
            context,
            filter_assets=True,
            init_operator_settings_arguments={"from_current_file": LibraryType.is_file_current(context)},
        )
