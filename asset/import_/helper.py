import os.path
from pathlib import Path
import bpy
from asset_browser_utilities.library.helper import append_asset, get_blend_library_name, item_exists
from asset_browser_utilities.file.save import create_new_file_and_set_as_current
from asset_browser_utilities.core.ui.message import message_box

from asset_browser_utilities.core.preferences.helper import get_from_cache, write_to_cache
from asset_browser_utilities.filter.main import AssetFilterSettings


class BatchHelper:
    def __init__(self, target_filepath, blend_filepaths, from_command_line):
        self.target_filepath = target_filepath
        self.blends = blend_filepaths
        self.blend = None
        self.filenames = []
        self.directories = []
        self.filepaths = []
        # In theory we should be able to execute this in another blender instance,
        # But that would mean destructively saving the user preferences, which is bad.
        # Since we roundtrip back to the original file it's okay not being able to.
        self.from_command_line = from_command_line

    def execute(self):
        self.execute_next()

    def execute_next(self):
        if self.blends:
            self.blend = self.blends.pop(0)
            self.open_or_create_file(self.blend)
            bpy.app.timers.register(self.add_asset_paths, first_interval=0.1)
        else:
            if self.from_command_line:
                bpy.ops.wm.quit_blender()
            else:
                self.open_or_create_file(self.target_filepath)
                bpy.app.timers.register(self.append_assets, first_interval=0.1)

    def add_asset_paths(self):
        _filter = get_from_cache(AssetFilterSettings)
        assets = _filter.get_objects_that_satisfy_filters()
        for asset in assets:
            self.filepaths.append(str(self.blend))
            self.directories.append(str(get_blend_library_name(asset)))
            self.filenames.append(str(asset.name))
        self.execute_next()

    def append_assets(self):
        for filepath, directory, filename in zip(self.filepaths, self.directories, self.filenames):
            append_asset(filepath, directory, filename)        
        message_box(message="Work completed !")

    def open_or_create_file(self, filepath):
        if os.path.isfile(filepath):
            bpy.ops.wm.open_mainfile(filepath=str(filepath))
        else:
            create_new_file_and_set_as_current(str(filepath))
