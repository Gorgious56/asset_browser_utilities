from asset_browser_utilities.core.test.prop import TestOperator
import bpy

from asset_browser_utilities.module.asset.tool import get_selected_asset_files_cache
from asset_browser_utilities.module.asset.operator.copy import AssetCopyDataExecute
from asset_browser_utilities.core.filter.type import get_types

from asset_browser_utilities.module.asset.tool import is_asset


def assert_that_two_assets_data_share_the_same_property(a, b, prop_name):
    assert getattr(a, prop_name) == getattr(
        b, prop_name
    ), f"{repr(a.id_data)}'s {prop_name} should be the same as {repr(b.id_data)}"


def assert_that_two_assets_data_share_the_same_catalog(a, b):
    assert_that_two_assets_data_share_the_same_property(a, b, "catalog_id")


def assert_that_two_assets_data_share_the_same_description(a, b):
    assert_that_two_assets_data_share_the_same_property(a, b, "description")


def assert_that_two_assets_data_share_the_same_author(a, b):
    assert_that_two_assets_data_share_the_same_property(a, b, "author")


def assert_that_two_assets_data_share_the_same_preview(a, b):
    assert list(a.id_data.preview.image_size) == list(
        b.id_data.preview.image_size
    ), f"{repr(a.id_data)} and {b.id_data} should have the same preview size"
    for pxl_a, pxl_b in zip(a.id_data.preview.image_pixels, b.id_data.preview.image_pixels):
        assert pxl_a == pxl_b, f"{repr(a.id_data)} and {b.id_data} should have the same preview pixels"


def assert_that_a_has_at_as_least_the_same_tags_as_b(a, b):
    tags_to = [tag.name for tag in a.tags]
    for tag in b.tags:
        assert tag.name in tags_to, f"{repr(a.id_data)} should have the same tags as {b.id_data}"


def assert_that_a_has_at_as_least_the_same_custom_props_as_b(a, b):
    for custom_prop in b.keys():
        assert custom_prop in a, f"{repr(a.id_data)} should have the same custom props as {b.id_data}"


def test_copying_all_props_from_active_to_selected_in_current_file(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=True,
        op_name="op_copy_data",
        logic_class=AssetCopyDataExecute,
    )

    test_op.op_props.tags = True
    test_op.op_props.custom_properties = True
    test_op.op_props.preview = True
    test_op.op_props.catalog = True
    test_op.op_props.author = True
    test_op.op_props.description = True

    asset_copy_from_name = "asset_copy_from"
    selected_asset_files = get_selected_asset_files_cache()
    selected_asset_files.set_active("object", bpy.data.objects[asset_copy_from_name])

    supported_asset_types = [a_t[0] for a_t in get_types()]
    for d in dir(bpy.data):
        container = getattr(bpy.data, d)
        if "bpy_prop_collection" in str(type(container)):
            if d in supported_asset_types:
                for asset in container:
                    if asset == bpy.data.objects[asset_copy_from_name]:
                        continue
                    else:
                        selected_asset_files.add(d, asset)

    test_op.execute()

    asset_from = bpy.data.objects[asset_copy_from_name]
    asset_data_from = asset_from.asset_data
    for asset_to_file in selected_asset_files.files_prop:
        asset_to = getattr(bpy.data, asset_to_file.container)[asset_to_file.name]
        if not is_asset(asset_to):
            continue
        asset_data_to = asset_to.asset_data
        assert_that_two_assets_data_share_the_same_catalog(asset_data_to, asset_data_from)
        assert_that_two_assets_data_share_the_same_description(asset_data_to, asset_data_from)
        assert_that_two_assets_data_share_the_same_author(asset_data_to, asset_data_from)
        assert_that_two_assets_data_share_the_same_preview(asset_data_to, asset_data_from)
        assert_that_a_has_at_as_least_the_same_tags_as_b(asset_data_to, asset_data_from)
        assert_that_a_has_at_as_least_the_same_custom_props_as_b(asset_data_to, asset_data_from)
