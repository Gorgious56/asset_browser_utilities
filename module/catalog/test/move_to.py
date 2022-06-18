from pathlib import Path
import bpy
from asset_browser_utilities.module.catalog.tool import CatalogsHelper
from asset_browser_utilities.core.test.prop import TestOperator
from asset_browser_utilities.module.catalog.operator.move_to import (
    CatalogMoveOperatorProperties,
    CatalogMovetoBatchExecute,
)

from asset_browser_utilities.module.asset.tool import all_assets
from asset_browser_utilities.module.catalog.test.tool import CATALOG_TO_UUID, assert_that_asset_is_in_catalog


def test_moving_all_assets_to_an_already_existing_catalog(filepath):
    for mode in CatalogMoveOperatorProperties.bl_rna.properties["mode"].enum_items:
        mode = mode.name
        print(f"      Test moving assets under mode '{mode}'")
        test_op = TestOperator(
            filepath=filepath,
            filter_assets=True,
            op_name="op_catalog_move",
            logic_class=CatalogMovetoBatchExecute,
        )

        bpy.ops.wm.open_mainfile(filepath=str(filepath))

        test_op.op_props.mode = mode
        test_op.op_props.catalog_name = "Test"
        test_op.op_props.catalog.allow = True
        test_op.op_props.catalog.active = True
        test_op.op_props.catalog.catalog = CATALOG_TO_UUID

        test_op.execute()

        helper = CatalogsHelper()
        for asset in all_assets():
            if mode == "Existing":
                uuid = CATALOG_TO_UUID
            elif mode == "New":
                uuid = helper.ensure_or_create_catalog_definition(test_op.op_props.catalog_name)
            elif mode == "File name":
                uuid = helper.ensure_or_create_catalog_definition(Path(bpy.data.filepath).stem)
            elif mode == "Asset name":
                uuid = helper.ensure_or_create_catalog_definition(asset.name)
            elif mode == "Collection name":
                if (
                    hasattr(asset, "users_collection")
                    and len(asset.users_collection) > 0
                    and asset.users_collection[0] is not None
                ):
                    uuid = helper.ensure_or_create_catalog_definition(asset.users_collection[0].name)
                else:
                    continue
            elif mode == "Material name":
                if (
                    hasattr(asset, "material_slots")
                    and len(asset.material_slots) > 0
                    and asset.material_slots[0].material is not None
                ):
                    uuid = helper.ensure_or_create_catalog_definition(asset.material_slots[0].material.name)
                else:
                    continue
            elif mode == "Asset data name":
                if hasattr(asset, "data") and asset.data is not None:
                    uuid = helper.ensure_or_create_catalog_definition(asset.data.name or "Catalog")
                else:
                    continue
            assert_that_asset_is_in_catalog(asset, uuid)
