from asset_browser_utilities.core.log.logger import Logger
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, StringProperty

from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps
from asset_browser_utilities.core.filter.catalog import FilterCatalog
from asset_browser_utilities.module.catalog.tool import CatalogsHelper
from asset_browser_utilities.core.file.path import get_current_file_path


class CatalogMoveFromAToBOperatorProperties(PropertyGroup, BaseOperatorProps):
    catalog_from: PointerProperty(type=FilterCatalog)
    catalog_to: PointerProperty(type=FilterCatalog)

    def init(self, from_current_file=False):
        for catalog in (self.catalog_from, self.catalog_to):
            catalog.active = True
            catalog.from_current_file = from_current_file
            catalog.catalog_filepath = str(CatalogsHelper().catalog_filepath)

    def draw(self, layout, context=None):
        box = layout.box()
        box.label(text="Move Assets :")
        for catalog, label in zip((self.catalog_from, self.catalog_to), ("FROM", "TO")):
            split = box.split(factor=0.35)
            split.label(text=label)
            split.prop(catalog, catalog.catalog_attribute, icon="ASSET_MANAGER", text="")

    def run_in_file(self, attributes=None):
        helper = CatalogsHelper()
        uuid_from, tree_from, name_from = helper.catalog_info_from_uuid(self.catalog_from.catalog)
        uuid_to, tree_to, name_to = helper.catalog_info_from_uuid(self.catalog_to.catalog)
        if uuid_from != uuid_to:
            helper.ensure_catalog_exists(uuid_to, tree_to, name_to)
            for asset in self.get_assets():
                asset_data = asset.asset_data
                if asset_data.catalog_id == uuid_from:
                    asset_data.catalog_id = uuid_to
                    Logger.display(
                        f"{get_current_file_path()} : {repr(asset)} moved from catalog '{name_from}' to catalog '{name_to}'"
                    )


class ABU_OT_catalog_move_from_a_to_b(Operator, BatchFolderOperator):
    bl_idname = "abu.catalog_move_from_a_to_b"
    bl_label = "Batch Move Assets From One Catalog to Another One"

    operator_settings: PointerProperty(type=CatalogMoveFromAToBOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context)
