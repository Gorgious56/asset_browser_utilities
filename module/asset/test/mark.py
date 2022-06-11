from asset_browser_utilities.module.asset.test.tool import assert_that_id_is_an_asset, assert_that_id_is_not_an_asset
import bpy

from asset_browser_utilities.core.test.tool import (
    execute_logic,
    get_asset_filter_settings,
    set_library_export_source,
    setup_and_get_current_operator,
)

from asset_browser_utilities.core.filter.type import get_object_types, get_types
from asset_browser_utilities.core.library.prop import LibraryType
from asset_browser_utilities.module.asset.operator.mark import AssetMarkBatchExecute

from asset_browser_utilities.module.asset.tool import all_assets_container_and_name


def setup_and_get_current_operator_():
    return setup_and_get_current_operator("mark_op")


def test_marking_all_assets_in_current_file(filepath):
    bpy.ops.wm.open_mainfile(filepath=str(filepath))

    set_library_export_source(LibraryType.FileCurrent.value)
    op_props = setup_and_get_current_operator_()
    op_props.generate_previews = False

    asset_filter_settings = get_asset_filter_settings()
    asset_filter_settings.filter_assets = False
    asset_filter_settings.filter_types.types_global_filter = False

    execute_logic(AssetMarkBatchExecute)

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
        bpy.ops.wm.open_mainfile(filepath=str(filepath))
        assets_start = all_assets_container_and_name()

        set_library_export_source(LibraryType.FileCurrent.value)

        op_props = setup_and_get_current_operator_()
        op_props.generate_previews = False

        asset_filter_settings = get_asset_filter_settings()
        asset_filter_settings.filter_assets = False
        asset_filter_settings.filter_types.types_global_filter = True
        asset_filter_settings.filter_types.types = {asset_type}
        asset_filter_settings.filter_types.types_object_filter = False

        execute_logic(AssetMarkBatchExecute)

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
        bpy.ops.wm.open_mainfile(filepath=str(filepath))
        assets_start = all_assets_container_and_name()

        set_library_export_source(LibraryType.FileCurrent.value)

        op_props = setup_and_get_current_operator_()
        op_props.generate_previews = False

        asset_filter_settings = get_asset_filter_settings()
        asset_filter_settings.filter_assets = False
        asset_filter_settings.filter_types.types_global_filter = True
        asset_filter_settings.filter_types.types = {"objects"}
        asset_filter_settings.filter_types.types_object_filter = True
        asset_filter_settings.filter_types.types_object = {object_type}

        execute_logic(AssetMarkBatchExecute)

        for obj in bpy.data.objects:
            if ("objects", obj.name) in assets_start:
                continue
            elif obj.type == object_type:
                assert_that_id_is_an_asset(obj)
            else:
                assert_that_id_is_not_an_asset(obj)
