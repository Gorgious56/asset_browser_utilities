import bpy.app.timers
from asset_browser_utilities.core.ui.message import message_box
from asset_browser_utilities.core.helper import copy_simple_property_group
from asset_browser_utilities.file.path import open_file_if_different_from_current, save_file_as
from asset_browser_utilities.preview.helper import is_preview_generated


class BatchExecute:
    INTERVAL = 0.2

    def __init__(self, blends, operator_settings, filter_settings, library_settings, callback):
        if operator_settings is not None:
            copy_simple_property_group(operator_settings, self)

        self.remove_backup = library_settings.remove_backup
        self.filter_settings = filter_settings

        self.blends = blends
        self.blend = None
        self.callback = callback  # This is called when everything is finished.
        self.assets = []

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

    def save_file(self):
        save_file_as(str(self.blend), remove_backup=self.remove_backup)

    def open_next_blend(self):
        self.blend = self.blends.pop(0)
        open_file_if_different_from_current(str(self.blend))

    def sleep_until_previews_are_done_and_execute_next_file(self):
        while self.assets:  # Check if all previews have been generated
            if is_preview_generated(self.assets[0]):
                self.assets.pop(0)
            else:
                return self.INTERVAL
        print("All previews have been generated !")
        self.save_file()
        self.execute_next_blend()
        return None
