from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.library.execute import BatchExecute
from asset_browser_utilities.library.operator import BatchOperator
from asset_browser_utilities.catalog.helper import (
    get_catalog_line_from_uuid,
    get_catalog_info_from_line,
    ensure_catalog_exists,
)
from asset_browser_utilities.catalog.prop import FilterCatalog


class BatchRemoveFromCatalog(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        uuid, _, _ = get_catalog_info_from_line(self.catalog_line)
        for asset in self.assets:
            if asset.asset_data.catalog_id == uuid:
                asset.asset_data.catalog_id = ""
        self.save_file()
        self.execute_next_blend()


class OperatorProperties(PropertyGroup):
    catalog: PointerProperty(type=FilterCatalog)
    catalog_line: StringProperty()

    def draw(self, layout):
        box = layout.box()
        box.label(text="Remove Assets From This Catalog")
        box.prop(self.catalog, "catalog", icon="ASSET_MANAGER")


class ASSET_OT_batch_move_to_catalog(Operator, ImportHelper, BatchOperator):
    "Batch Remove Assets From Catalog"
    bl_idname = "asset.batch_remove_from_catalog"
    bl_label = "Batch Remove From Catalog"

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchRemoveFromCatalog

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)

    def execute(self, context):
        self.operator_settings.catalog_line = get_catalog_line_from_uuid(self.operator_settings.catalog.catalog)
        return super().execute(context)
