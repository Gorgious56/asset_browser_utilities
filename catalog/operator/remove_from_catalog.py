from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty, BoolProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.filter.catalog import FilterCatalog
from asset_browser_utilities.catalog.tool import CatalogsHelper


class BatchRemoveFromCatalog(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        helper = CatalogsHelper()
        if self.filter:
            uuid, _, _ = helper.get_catalog_info_from_line(self.catalog_line)
            for asset in self.assets:
                if asset.asset_data.catalog_id == uuid:
                    asset.asset_data.catalog_id = ""
        else:
            for asset in self.assets:
                asset.asset_data.catalog_id = ""
        self.save_file()
        self.execute_next_blend()


class OperatorProperties(PropertyGroup):
    filter: BoolProperty(default=True, description="")
    catalog: PointerProperty(type=FilterCatalog)
    catalog_line: StringProperty()

    def draw(self, layout):
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Remove Assets From This Catalog" if self.filter else "Remove Assets From All Catalogs")
        row.prop(self, "filter", icon="FILTER", text="")
        if self.filter:
            box.prop(self.catalog, "catalog", icon="ASSET_MANAGER")


class ASSET_OT_batch_move_to_catalog(Operator, BatchFolderOperator):
    "Batch Remove Assets From Catalog"
    bl_idname = "asset.batch_remove_from_catalog"
    bl_label = "Batch Remove From Catalog"

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchRemoveFromCatalog

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)

    def execute(self, context):
        helper = CatalogsHelper()
        self.operator_settings.catalog_line = helper.get_catalog_line_from_uuid(self.operator_settings.catalog.catalog)
        return super().execute(context)
