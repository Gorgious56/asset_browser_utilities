from pathlib import Path
import os
import bpy

from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.test.prop import TestOperator

from asset_browser_utilities.module.preview.operator.extract import PreviewExtractBatchExecute
from asset_browser_utilities.core.filter.main import AssetFilterSettings


def test_extracting_previews(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=True,
        logic_class=PreviewExtractBatchExecute,
    )
    asset_filter_settings = get_from_cache(AssetFilterSettings)
    asset_filter_settings.types_global_filter = False
    asset_filter_settings.filter_name.active = True
    asset_filter_settings.filter_name.method = "Contains"
    asset_filter_settings.filter_name.value = "mesh"

    folder = Path(bpy.data.filepath).parent
    asset_paths = []
    for asset in asset_filter_settings.get_objects_that_satisfy_filters():
        if not asset.preview.image_pixels_float:
            continue
        asset_paths.append(folder / (asset.name + ".png"))
        assert not (asset_paths[-1]).exists(), f"Image '{str(asset_paths[-1])}' should not exist at this point"

    test_op.execute()
    for asset_path in asset_paths:
        assert asset_path.exists(), f"Image '{str(asset_path)}' should exist at this point"
        os.remove(str(asset_path))

    asset_filter_settings.filter_name.active = False
