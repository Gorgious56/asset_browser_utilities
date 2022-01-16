import bpy.app.timers
from asset_browser_utilities.library.execute import BatchExecute


class BatchGeneratePreviews(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        print(self.assets)
        for i in range(len(self.assets) - 1, -1, -1):
            if self.assets[i].asset_data is not None:
                asset = self.assets[i]
                asset.asset_generate_preview()

        bpy.app.timers.register(self.sleep_until_previews_are_done_and_execute_next_file)
