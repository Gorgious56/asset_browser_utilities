from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.core.filter.catalog import FilterCatalog
from asset_browser_utilities.module.catalog.tool import CatalogsHelper


class CatalogMoveFromAToBBatchExecute(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        op_props = get_current_operator_properties()
        helper = CatalogsHelper()
        uuid_from, tree_from, name_from = helper.catalog_info_from_uuid(op_props.catalog_from.catalog)
        uuid_to, tree_to, name_to = helper.catalog_info_from_uuid(op_props.catalog_to.catalog)
        if uuid_from != uuid_to:
            helper.ensure_catalog_exists(uuid_to, tree_to, name_to)
            for asset in self.assets:
                asset_data = asset.asset_data
                if asset_data.catalog_id == uuid_from:
                    asset_data.catalog_id = uuid_to
                    Logger.display(f"{repr(asset)} moved from catalog '{name_from}' to catalog '{name_to}'")
            self.save_file()
        self.execute_next_blend()


class CatalogMoveFromAToBOperatorProperties(PropertyGroup):
    catalog_from: PointerProperty(type=FilterCatalog)
    catalog_to: PointerProperty(type=FilterCatalog)

    def draw(self, layout):
        box = layout.box()
        box.label(text="Move Assets :")
        split = box.split(factor=0.35)
        split.label(text="FROM")
        split.prop(self.catalog_from, "catalog", icon="ASSET_MANAGER", text="")
        split = box.split(factor=0.35)
        split.label(text="TO")
        split.prop(self.catalog_to, "catalog", icon="ASSET_MANAGER", text="")
        self.catalog_from.draw_filepath(box)


class ABU_OT_catalog_move_from_a_to_b(Operator, BatchFolderOperator):
    bl_idname = "abu.catalog_move_from_a_to_b"
    bl_label = "Batch Move Assets From One Catalog to Another One"

    operator_settings: PointerProperty(type=CatalogMoveFromAToBOperatorProperties)
    logic_class = CatalogMoveFromAToBBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
