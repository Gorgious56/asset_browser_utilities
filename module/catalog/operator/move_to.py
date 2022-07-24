from pathlib import Path
import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, EnumProperty, StringProperty

from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator
from asset_browser_utilities.core.filter.catalog import FilterCatalog

from asset_browser_utilities.module.catalog.tool import CatalogsHelper


class CatalogMovetoBatchExecute(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        op_props = get_current_operator_properties()
        if op_props.mode in ("Existing", "New", "File name"):
            uuid, name = self.get_catalog_uuid_and_name(op_props)
            for asset in self.assets:
                if uuid is None or name is None:
                    continue
                asset.asset_data.catalog_id = uuid
                Logger.display(f"{repr(asset)} moved to catalog '{name}'")
        else:
            for asset in self.assets:
                uuid, name = self.get_catalog_uuid_and_name(op_props, asset)
                if uuid is None or name is None:
                    continue
                asset.asset_data.catalog_id = uuid
                Logger.display(f"{repr(asset)} moved to catalog '{name}'")

        self.save_file()
        self.execute_next_blend()

    def get_catalog_uuid_and_name(self, op_props, asset=None):
        uuid, name = None, None
        helper = CatalogsHelper()
        if op_props.mode == "Existing":
            uuid, tree, name = helper.catalog_info_from_uuid(op_props.catalog.catalog)
            helper.ensure_catalog_exists(uuid, tree, name)
        elif op_props.mode == "New":
            uuid = helper.ensure_or_create_catalog_definition(op_props.catalog_name or "Catalog")
        elif op_props.mode == "File name":
            uuid = helper.ensure_or_create_catalog_definition(Path(bpy.data.filepath).stem or "Catalog")
        elif op_props.mode == "Asset name":
            uuid = helper.ensure_or_create_catalog_definition(asset.name or "Catalog")
        elif op_props.mode == "Collection name":
            if (
                hasattr(asset, "users_collection")
                and len(asset.users_collection) > 0
                and asset.users_collection[0] is not None
            ):
                uuid = helper.ensure_or_create_catalog_definition(asset.users_collection[0].name or "Catalog")
            elif isinstance(asset, bpy.types.Collection):
                parent = next((c for c in bpy.data.collections if c.user_of_id(asset)), None)
                if parent:
                    uuid = helper.ensure_or_create_catalog_definition(parent.name or "Catalog")
        elif op_props.mode == "Material name":
            if (
                hasattr(asset, "material_slots")
                and len(asset.material_slots) > 0
                and asset.material_slots[0].material is not None
            ):
                uuid = helper.ensure_or_create_catalog_definition(asset.material_slots[0].material.name)
        elif op_props.mode == "Asset data name":
            if hasattr(asset, "data") and asset.data is not None:
                uuid = helper.ensure_or_create_catalog_definition(asset.data.name or "Catalog")
        if uuid is not None:
            uuid, tree, name = helper.catalog_info_from_uuid(uuid)
        return uuid, name


class CatalogMoveOperatorProperties(PropertyGroup):
    mode: EnumProperty(
        name="Destination",
        items=(
            ("Existing",) * 3,
            ("New",) * 3,
            ("File name",) * 3,
            ("Asset name",) * 3,
            ("Collection name",) * 3,
            ("Material name",) * 3,
            ("Asset data name",) * 3,
        ),
    )
    catalog: PointerProperty(type=FilterCatalog)
    catalog_name: StringProperty(name="Name")

    def draw(self, layout, context=None):
        box = layout.box()
        box.label(text="Move Assets to This Catalog")
        box.prop(self, "mode")
        if self.mode == "Existing":
            box.prop(self.catalog, "catalog", icon="ASSET_MANAGER")
            self.catalog.draw_filepath(box)
        elif self.mode == "New":
            box.prop(self, "catalog_name")


class ABU_OT_catalog_move(Operator, BatchFolderOperator):
    bl_idname = "abu.catalog_move"
    bl_label = "Batch Move To Catalog"

    operator_settings: PointerProperty(type=CatalogMoveOperatorProperties)
    logic_class = CatalogMovetoBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
