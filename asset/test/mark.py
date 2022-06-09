from asset_browser_utilities.filter.type import get_object_types, get_types
import bpy

from asset_browser_utilities.core.cache.tool import get_cache, get_current_operator_properties, get_from_cache
from asset_browser_utilities.core.operator.prop import CurrentOperatorProperty
from asset_browser_utilities.filter.main import AssetFilterSettings
from asset_browser_utilities.library.prop import LibraryExportSettings, LibraryType
from asset_browser_utilities.asset.operator.mark import AssetMarkBatchExecute

from asset_browser_utilities.asset.tool import all_assets, is_asset


def execute_logic():
    logic = AssetMarkBatchExecute()
    logic.save_file = lambda: None
    logic.execute_next_blend()


def test_marking_all_assets_in_current_file(filepath):
        bpy.ops.wm.open_mainfile(filepath=str(filepath))

        get_from_cache(LibraryExportSettings).source = LibraryType.FileCurrent.value

        get_from_cache(CurrentOperatorProperty).class_name = str(get_cache().mark_op.__class__)
        op_props = get_current_operator_properties()
        op_props.generate_previews = False

        asset_filter_settings = get_from_cache(AssetFilterSettings)
        asset_filter_settings.filter_assets = False
        asset_filter_settings.filter_types.types_global_filter = False
        
        execute_logic()

        supported_asset_types = [a_t[0] for a_t in get_types()]
        for d in dir(bpy.data):
            container = getattr(bpy.data, d)
            if "bpy_prop_collection" in str(type(container)):
                if d in supported_asset_types:
                    for asset in container:
                        assert is_asset(asset), f"'bpy.data.{d}.{asset.name}' should be an asset."
                else:
                    for asset in container:
                        assert not is_asset(asset), f"'bpy.data.{d}.{asset.name}' should not be an asset."
                    
    
def test_marking_different_asset_types_in_current_file(filepath):
    for asset_type_tuple in get_types():
        asset_type = asset_type_tuple[0]
        bpy.ops.wm.open_mainfile(filepath=str(filepath))
        assets_start = all_assets()

        get_from_cache(LibraryExportSettings).source = LibraryType.FileCurrent.value

        get_from_cache(CurrentOperatorProperty).class_name = str(get_cache().mark_op.__class__)
        op_props = get_current_operator_properties()
        op_props.generate_previews = False

        asset_filter_settings = get_from_cache(AssetFilterSettings)
        asset_filter_settings.filter_assets = False
        asset_filter_settings.filter_types.types_global_filter = True
        asset_filter_settings.filter_types.types = {asset_type}
        asset_filter_settings.filter_types.types_object_filter = False

        execute_logic()

        for d in dir(bpy.data):
            container = getattr(bpy.data, d)
            if "bpy_prop_collection" in str(type(container)):
                if d == asset_type:
                    for asset in container:
                        if asset.name in assets_start:
                            continue
                        assert is_asset(asset), f"'bpy.data.{d}.{asset.name}' should be an asset."
                else:
                    for asset in container:
                        if asset.name in assets_start:
                            continue
                        assert not is_asset(asset), f"'bpy.data.{d}.{asset.name}' should not be an asset."


def test_marking_different_object_types_in_current_file(filepath):
    for object_type_tuple in get_object_types():
        object_type = object_type_tuple[0]
        bpy.ops.wm.open_mainfile(filepath=str(filepath))
        assets_start = all_assets()

        get_from_cache(LibraryExportSettings).source = LibraryType.FileCurrent.value

        get_from_cache(CurrentOperatorProperty).class_name = str(get_cache().mark_op.__class__)
        op_props = get_current_operator_properties()
        op_props.generate_previews = False

        asset_filter_settings = get_from_cache(AssetFilterSettings)
        asset_filter_settings.filter_assets = False
        asset_filter_settings.filter_types.types_global_filter = True
        asset_filter_settings.filter_types.types = {"objects"}
        asset_filter_settings.filter_types.types_object_filter = True
        asset_filter_settings.filter_types.types_object = {object_type}

        execute_logic()

        for obj in bpy.data.objects:
            if obj.name in assets_start:
                continue
            if obj.type == object_type:
                assert is_asset(obj)
            else:
                assert not is_asset(obj)
