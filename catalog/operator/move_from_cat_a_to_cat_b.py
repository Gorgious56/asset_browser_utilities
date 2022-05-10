from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.filter.catalog import FilterCatalog
from asset_browser_utilities.catalog.tool import CatalogsHelper


class BatchMoveFromCatalogToCatalog(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        helper = CatalogsHelper()
        uuid_from, tree_from, name_from = helper.get_catalog_info_from_line(self.catalog_from_line)
        uuid_to, tree_to, name_to = helper.get_catalog_info_from_line(self.catalog_to_line)
        if uuid_from != uuid_to:
            helper.ensure_catalog_exists(uuid_to, tree_to, name_to)
            for asset in self.assets:
                asset_data = asset.asset_data
                if asset_data.catalog_id == uuid_from:
                    asset_data.catalog_id = uuid_to
            self.save_file()
        self.execute_next_blend()


class OperatorProperties(PropertyGroup):
    catalog_from: PointerProperty(type=FilterCatalog)
    catalog_from_line: StringProperty()
    catalog_to: PointerProperty(type=FilterCatalog)
    catalog_to_line: StringProperty()

    def draw(self, layout):
        box = layout.box()
        box.label(text="Move Assets :")
        split = box.split(factor=0.35)
        split.label(text="FROM")
        split.prop(self.catalog_from, "catalog", icon="ASSET_MANAGER", text="")
        split = box.split(factor=0.35)
        split.label(text="TO")
        split.prop(self.catalog_to, "catalog", icon="ASSET_MANAGER", text="")


class ASSET_OT_batch_move_from_cat_a_to_cat_b(Operator, BatchFolderOperator):
    "Batch Move Assets From One Catalog to Another One"
    bl_idname = "asset.batch_move_from_cat_a_to_cat_b"
    bl_label = "Batch Move Assets From One Catalog to Another One"

    operator_settings: PointerProperty(type=OperatorProperties)
    logic_class = BatchMoveFromCatalogToCatalog

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)

    def execute(self, context):
        helper = CatalogsHelper()
        self.operator_settings.catalog_from_line = helper.get_catalog_line_from_uuid(
            self.operator_settings.catalog_from.catalog
        )
        self.operator_settings.catalog_to_line = helper.get_catalog_line_from_uuid(
            self.operator_settings.catalog_to.catalog
        )
        return super().execute(context)
