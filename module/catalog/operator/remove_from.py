from asset_browser_utilities.core.cache.tool import get_current_operator_properties, get_from_cache
from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType
from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty, BoolProperty

from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.core.filter.catalog import FilterCatalog
from asset_browser_utilities.module.catalog.tool import CatalogsHelper


class CatalogRemoveFromBatchExecute(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        helper = CatalogsHelper()
        op_props = get_current_operator_properties()
        if op_props.filter:
            uuid, _, name = helper.catalog_info_from_uuid(op_props.catalog.catalog)
            for asset in self.assets:
                if asset.asset_data.catalog_id == uuid:
                    asset.asset_data.catalog_id = ""
                    Logger.display(f"{repr(asset)} unassigned from catalog '{name}'")
        else:
            for asset in self.assets:
                asset.asset_data.catalog_id = ""
                Logger.display(f"{repr(asset)} unassigned from its catalog")
        self.save_file()
        self.execute_next_blend()


class CatalogRemoveFromOperatorProperties(PropertyGroup):
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


class ABU_OT_catalog_remove_from(Operator, BatchFolderOperator):
    bl_idname = "abu.catalog_remove_from"
    bl_label = "Batch Remove From Catalog"

    operator_settings: PointerProperty(type=CatalogRemoveFromOperatorProperties)
    logic_class = CatalogRemoveFromBatchExecute

    def invoke(self, context, event):
        return self._invoke(
            context,
            filter_assets=True,
            init_operator_settings_arguments={"from_current_file": LibraryType.is_file_current(context)},
        )
