from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.core.filter.catalog import FilterCatalog
from asset_browser_utilities.module.catalog.tool import CatalogsHelper


class BatchMoveToCatalog(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        op_props = get_current_operator_properties()
        helper = CatalogsHelper()
        uuid, tree, name = helper.catalog_info_from_uuid(op_props.catalog.catalog)
        helper.ensure_catalog_exists(uuid, tree, name)
        for asset in self.assets:
            asset.asset_data.catalog_id = uuid
            Logger.display(f"'{asset.name}' moved to catalog '{name}'")
        self.save_file()
        self.execute_next_blend()


class CatalogMoveOperatorProperties(PropertyGroup):
    catalog: PointerProperty(type=FilterCatalog)

    def draw(self, layout):
        box = layout.box()
        box.label(text="Move Assets to This Catalog")
        box.prop(self.catalog, "catalog", icon="ASSET_MANAGER")
        self.catalog.draw_filepath(box)


class ABU_OT_catalog_move(Operator, BatchFolderOperator):
    bl_idname = "abu.catalog_move"
    bl_label = "Batch Move To Catalog"

    operator_settings: PointerProperty(type=CatalogMoveOperatorProperties)
    logic_class = BatchMoveToCatalog

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
