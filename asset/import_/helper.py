import os.path
from pathlib import Path
import bpy
from asset_browser_utilities.library.helper import item_exists
from asset_browser_utilities.file.save import (
    create_new_file_and_set_as_current,
    save_file,
)
from asset_browser_utilities.core.ui.message import message_box

from asset_browser_utilities.core.preferences.helper import get_from_cache, write_to_cache
from asset_browser_utilities.filter.main import AssetFilterSettings
from asset_browser_utilities.asset.import_.prop import CacheAssetPaths


class BatchExecute:
    def __init__(self, blend_filepaths):
        self.blends = blend_filepaths
        self.blend = None

    def execute(self):
        self.execute_next()

    def execute_next(self):
        if self.blends:
            self.blend = self.blends.pop(0)
            self.open_or_create_file(self.blend)
            bpy.app.timers.register(self.add_asset_paths, first_interval=0.1)
        else:
            bpy.ops.wm.quit_blender()

    def add_asset_paths(self):
        cache = get_from_cache(CacheAssetPaths)
        filter = get_from_cache(AssetFilterSettings)
        print(filter)
        print(filter.filter_types.items)
        assets = filter.get_objects_that_satisfy_filters()
        print(assets)
        self.execute_next()

    def open_or_create_file(self, filepath=None):
        if filepath is None:
            filepath = self.filepath
        if os.path.isfile(filepath):
            bpy.ops.wm.open_mainfile(filepath=str(filepath))
        else:
            create_new_file_and_set_as_current(str(filepath))
