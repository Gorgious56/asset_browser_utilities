from pathlib import Path
import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, EnumProperty, StringProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps
from asset_browser_utilities.core.filter.catalog import FilterCatalog

from asset_browser_utilities.module.catalog.tool import CatalogsHelper


class CatalogMoveOperatorProperties(PropertyGroup, BaseOperatorProps):
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

    def init(self, from_current_file=False):
        self.catalog.active = True
        self.catalog.from_current_file = from_current_file
        self.catalog.catalog_filepath = str(CatalogsHelper().catalog_filepath)

    def draw(self, layout, context=None):
        box = layout.box()
        box.label(text="Move Assets to This Catalog")
        box.prop(self, "mode")
        if self.mode == "Existing":
            self.catalog.draw(box, context, draw_filter=False)
        elif self.mode == "New":
            box.prop(self, "catalog_name")

    def run_in_file(self, attributes=None):
        assets = self.get_assets()
        if not assets:
            return
        if self.mode in ("Existing", "New", "File name"):
            uuid, name = self.get_catalog_uuid_and_name()
            for asset in assets:
                if uuid is None or name is None:
                    continue
                asset.asset_data.catalog_id = uuid
                Logger.display(f"{repr(asset)} moved to catalog '{name}'")
        else:
            for asset in assets:
                uuid, name = self.get_catalog_uuid_and_name(asset)
                if uuid is None or name is None:
                    continue
                asset.asset_data.catalog_id = uuid
                Logger.display(f"{repr(asset)} moved to catalog '{name}'")

    def get_catalog_uuid_and_name(self, asset=None):
        uuid, name = None, None
        helper = CatalogsHelper()
        if self.mode == "Existing":
            uuid, tree, name = helper.catalog_info_from_uuid(self.catalog.catalog)
            helper.ensure_catalog_exists(uuid, tree, name)
        elif self.mode == "New":
            uuid = helper.ensure_or_create_catalog_definition(self.catalog_name or "Catalog")
        elif self.mode == "File name":
            uuid = helper.ensure_or_create_catalog_definition(Path(bpy.data.filepath).stem or "Catalog")
        elif self.mode == "Asset name":
            uuid = helper.ensure_or_create_catalog_definition(asset.name or "Catalog")
        elif self.mode == "Collection name":
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
        elif self.mode == "Material name":
            if (
                hasattr(asset, "material_slots")
                and len(asset.material_slots) > 0
                and asset.material_slots[0].material is not None
            ):
                uuid = helper.ensure_or_create_catalog_definition(asset.material_slots[0].material.name)
        elif self.mode == "Asset data name":
            if hasattr(asset, "data") and asset.data is not None:
                uuid = helper.ensure_or_create_catalog_definition(asset.data.name or "Catalog")
        if uuid is not None:
            uuid, tree, name = helper.catalog_info_from_uuid(uuid)
        return uuid, name


class ABU_OT_catalog_move(Operator, BatchFolderOperator):
    bl_idname = "abu.catalog_move"
    bl_label = "Batch Move To Catalog"

    operator_settings: PointerProperty(type=CatalogMoveOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
