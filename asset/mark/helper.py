import bpy
from asset_browser_utilities.library.execute import BatchExecute


class BatchUnmark(BatchExecute):
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


class BatchMark(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        if not self.assets:
            self.execute_next_blend()
            return

        if self.generate_previews:
            self.mark_assets_with_previews()
        else:
            self.mark_assets_without_previews()

    def mark_assets_with_previews(self):
        for asset in self.assets:
            asset.asset_mark()
            asset.asset_generate_preview()
            print(f"Mark {asset.name}")
        bpy.app.timers.register(self.sleep_until_previews_are_done_and_execute_next_file)

    def mark_assets_without_previews(self):
        [asset.asset_mark() for asset in self.assets]
        print(f"Mark {len(self.assets)} assets without previews")
        self.save_file()
        self.execute_next_blend()
