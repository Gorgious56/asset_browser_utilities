from pathlib import Path
import os
from asset_browser_utilities.module.preview.operator.import_ import PreviewImportBatchExecute
import bpy

from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.core.test.prop import TestOperator

from asset_browser_utilities.module.asset.tool import all_assets
from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.library.prop import LibraryExportSettings


def test_importing_previews(filepath):
    test_op = TestOperator(
        filepath=filepath,
        filter_assets=True,
        logic_class=PreviewImportBatchExecute,
    )
    library_export_settings = get_from_cache(LibraryExportSettings)
    folder = Path(bpy.data.filepath).parent / "previews"
    library_export_settings.folder = str(folder)
    asset_filter_settings = get_from_cache(AssetFilterSettings)

    for asset in asset_filter_settings.get_objects_that_satisfy_filters():
        if not asset.preview.image_pixels_float:
            continue
        asset.asset_generate_preview()
        assert not any(asset.preview.image_pixels_float)

    test_op.execute()

    for asset in asset_filter_settings.get_objects_that_satisfy_filters():
        if not asset.preview.image_pixels_float:
            continue
        assert any(asset.preview.image_pixels_float), f"{repr(asset)} should have a preview"
