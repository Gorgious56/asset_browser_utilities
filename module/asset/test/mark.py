from asset_browser_utilities.core.test.prop import TestOperator
from asset_browser_utilities.module.asset.test.tool import assert_that_id_is_an_asset, assert_that_id_is_not_an_asset
import bpy

from asset_browser_utilities.core.filter.type import get_object_types, get_types
from asset_browser_utilities.module.asset.operator.mark import AssetMarkBatchExecute

from asset_browser_utilities.module.asset.tool import all_assets_container_and_name


def test_marking_all_assets_in_current_file(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=False,
        op_name="mark_op",
        logic_class=AssetMarkBatchExecute,
    )

    test_op.op_props.generate_previews = False

    test_op.execute()

    supported_asset_types = [a_t[0] for a_t in get_types()]
    for d in dir(bpy.data):
        container = getattr(bpy.data, d)
        if "bpy_prop_collection" in str(type(container)):
            if d in supported_asset_types:
                for asset in container:
                    assert_that_id_is_an_asset(asset)
            else:
                for asset in container:
                    assert_that_id_is_not_an_asset(asset)


def test_marking_different_asset_types_in_current_file(filepath):
    for asset_type_tuple in get_types():
        asset_type = asset_type_tuple[0]
        test_op = TestOperator(
            filepath=filepath,
            filter_assets=False,
            filter_types={asset_type},
            filter_object_types=False,
            op_name="mark_op",
            logic_class=AssetMarkBatchExecute,
        )
        assets_start = all_assets_container_and_name()

        test_op.op_props.generate_previews = False

        test_op.execute()

        for d in dir(bpy.data):
            container = getattr(bpy.data, d)
            if "bpy_prop_collection" in str(type(container)):
                if d == asset_type:
                    for asset in container:
                        if (d, asset.name) in assets_start:
                            continue
                        assert_that_id_is_an_asset(asset)
                else:
                    for asset in container:
                        if (d, asset.name) in assets_start:
                            continue
                        assert_that_id_is_not_an_asset(asset)


def test_marking_different_object_types_in_current_file(filepath):
    for object_type_tuple in get_object_types():
        object_type = object_type_tuple[0]
        test_op = TestOperator(
            filepath=filepath,
            filter_assets=False,
            filter_types={"objects"},
            filter_object_types={object_type},
            op_name="mark_op",
            logic_class=AssetMarkBatchExecute,
        )
        assets_start = all_assets_container_and_name()

        test_op.op_props.generate_previews = False

        test_op.execute()

        for obj in bpy.data.objects:
            if ("objects", obj.name) in assets_start:
                continue
            elif obj.type == object_type:
                assert_that_id_is_an_asset(obj)
            else:
                assert_that_id_is_not_an_asset(obj)
