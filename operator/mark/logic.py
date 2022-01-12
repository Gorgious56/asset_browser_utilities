import numpy as np
import bpy
from asset_browser_utilities.ui.message import message_box
from asset_browser_utilities.helper.path import (
    open_file_if_different_from_current,
    save_file_as
)


class OperatorLogic:
    INTERVAL = 0.2

    def __init__(self, blends, operator_settings, filter_settings):
        self.prevent_backup = operator_settings.prevent_backup
        self.overwrite = operator_settings.overwrite
        self.generate_previews = operator_settings.generate_previews
        self.force_previews = operator_settings.force_previews

        self.filter_settings = filter_settings

        self.blends = blends
        self.blend = None
        self.assets = []
        self.assets_to_only_preview = []

    def execute_next_blend(self):
        if not self.blends:
            print("Work completed")
            message_box(message="Work completed !")
            return
        print(f"{len(self.blends)} file{'s' if len(self.blends) > 1 else ''} left")

        self.open_next_blend()
        self.assets = self.filter_settings.get_objects_that_satisfy_filters()

        # Give slight delay otherwise stack overflow
        bpy.app.timers.register(self.execute_one_file_and_the_next_when_finished, first_interval=self.INTERVAL)


class OperatorLogicUnmark(OperatorLogic):
    def execute_one_file_and_the_next_when_finished(self):
        self.populate_assets()
        if self.assets:            
            self.unmark_assets()
            self.save_file()
        self.execute_next_blend()
    
    def populate_assets(self):
        self.assets = [a for a in self.assets if a.asset_data is not None]

    def unmark_assets(self):
        for asset in self.assets:
            asset.asset_clear()

    def save_file(self):
        save_file_as(str(self.blend), remove_backup=self.prevent_backup)

    def open_next_blend(self):
        self.blend = self.blends.pop(0)
        open_file_if_different_from_current(str(self.blend))


class OperatorLogicMark(OperatorLogic):
    def execute_one_file_and_the_next_when_finished(self):
        if not self.overwrite:
            for i in range(len(self.assets) - 1, -1, -1):
                if self.assets[i].asset_data is not None:
                    asset = self.assets.pop(i)
                    if self.force_previews:
                        asset.asset_generate_preview()
                        self.assets_to_only_preview.append(asset)

        if not self.assets and not self.assets_to_only_preview:  # We don't mark any asset, don't bother saving the file
            print("No asset to mark")
            self.execute_next_blend()
            return

        if self.generate_previews:
            self.mark_assets_with_previews()
        else:
            self.mark_assets_without_previews()

    def save_file(self):
        save_file_as(str(self.blend), remove_backup=self.prevent_backup)

    def open_next_blend(self):
        self.blend = self.blends.pop(0)
        open_file_if_different_from_current(str(self.blend))

    def mark_assets_with_previews(self):
        for asset in self.assets:
            asset.asset_mark()
            asset.asset_generate_preview()
            print(f"Mark {asset.name}")
        bpy.app.timers.register(self.sleep_until_previews_are_done)

    def sleep_until_previews_are_done(self):
        while self.assets:  # Check if all previews have been generated
            if self.is_preview_generated(self.assets[0]):
                self.assets.pop(0)
            else:
                return self.INTERVAL
        while self.assets_to_only_preview:  # Check if all previews have been generated
            if self.is_preview_generated(self.assets_to_only_preview[0]):
                self.assets_to_only_preview.pop(0)
            else:
                return self.INTERVAL
        print("All previews have been generated !")
        self.save_file()
        self.execute_next_blend()
        return None

    def is_preview_generated(self, asset):
        preview = asset.preview
        if not preview:
            asset.asset_generate_preview()
        arr = np.zeros((preview.image_size[0] * preview.image_size[1]) * 4, dtype=np.float32)
        preview.image_pixels_float.foreach_get(arr)
        return np.any((arr != 0))

    def mark_assets_without_previews(self):
        [asset.asset_mark() for asset in self.assets]
        print(f"Mark {len(self.assets)} assets without previews")
        self.save_file()
        self.execute_next_blend()

    def unmark_assets(self):
        self.assets = [a for a in self.assets if a.asset_data is not None]

        if not self.assets:  # We don't unmark any asset, don't bother saving the file
            print("No asset to unmark")
            return

        for asset in self.assets:
            asset.asset_clear()
            print(f"Unmark {asset.name}")

        self.save_file()
