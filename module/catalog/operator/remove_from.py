from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty, BoolProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.core.filter.catalog import FilterCatalog
from asset_browser_utilities.module.catalog.tool import CatalogsHelper


class BatchRemoveFromCatalog(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        helper = CatalogsHelper()
        op_props = get_current_operator_properties()
        if op_props.filter:
            uuid, _, name = helper.catalog_info_from_uuid(op_props.catalog.catalog)
            for asset in self.assets:
                if asset.asset_data.catalog_id == uuid:
                    asset.asset_data.catalog_id = ""
                    Logger.display(f"'{asset.name}' unassigned from catalog '{name}'")
        else:
            for asset in self.assets:
                asset.asset_data.catalog_id = ""
                Logger.display(f"{asset.name} unassigned from its catalog")
        self.save_file()
        self.execute_next_blend()


class CatalogRemoveFromOperatorProperties(PropertyGroup):
    filter: BoolProperty(default=True, description="")
    catalog: PointerProperty(type=FilterCatalog)

    def draw(self, layout):
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Remove Assets From This Catalog" if self.filter else "Remove Assets From All Catalogs")
        row.prop(self, "filter", icon="FILTER", text="")
        if self.filter:
            box.prop(self.catalog, "catalog", icon="ASSET_MANAGER")
        self.catalog.draw_filepath(box)


class ABU_OT_catalog_remove_from(Operator, BatchFolderOperator):
    bl_idname = "abu.catalog_remove_from"
    bl_label = "Batch Remove From Catalog"

    operator_settings: PointerProperty(type=CatalogRemoveFromOperatorProperties)
    logic_class = BatchRemoveFromCatalog

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
