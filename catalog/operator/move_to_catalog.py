from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.filter.catalog import FilterCatalog
from asset_browser_utilities.catalog.tool import CatalogsHelper


class BatchMoveToCatalog(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        helper = CatalogsHelper()
        uuid, tree, name = helper.get_catalog_info_from_line(self.catalog_line)
        helper.ensure_catalog_exists(uuid, tree, name)
        for asset in self.assets:
            asset.asset_data.catalog_id = uuid
        self.save_file()
        self.execute_next_blend()


class OperatorProperties(PropertyGroup):
    catalog: PointerProperty(type=FilterCatalog)
    catalog_line: StringProperty()

    def draw(self, layout):
        box = layout.box()
        box.label(text="Move Assets to This Catalog")
        box.prop(self.catalog, "catalog", icon="ASSET_MANAGER")


class ASSET_OT_batch_move_to_catalog(Operator, BatchFolderOperator):
    "Batch Move Assets To Catalog"
    bl_idname = "asset.batch_move_to_catalog"
    bl_label = "Batch Move To Catalog"

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchMoveToCatalog

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)

    def execute(self, context):
        helper = CatalogsHelper()
        self.operator_settings.catalog_line = helper.get_catalog_line_from_uuid(self.operator_settings.catalog.catalog)
        return super().execute(context)
