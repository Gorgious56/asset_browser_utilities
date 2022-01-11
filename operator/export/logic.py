import os.path
from pathlib import Path
import bpy
from asset_browser_utilities.helper.library import item_exists
from asset_browser_utilities.helper.path import (
    create_new_file_and_set_as_current,
    save_file,
)
from asset_browser_utilities.ui.message import message_box


class OperatorLogic:
    def __init__(
        self, asset_names, asset_types, source_file, target_filepath, prevent_backup, overwrite, individual_files
    ):
        self.asset_names = asset_names
        self.asset_types = asset_types
        self.current_asset_name = ""
        self.current_asset_type = ""

        self.source_file = source_file
        self.filepath = target_filepath
        self.target_folder = Path(self.filepath).parent

        self.prevent_backup = prevent_backup
        self.overwrite = overwrite
        self.individual_files = individual_files

    def execute(self):
        if self.individual_files:
            self.execute_next()
        else:
            self.execute_all()

    def execute_all(self):
        self.open_or_create_file(self.filepath)
        bpy.app.timers.register(self.append_all_assets_and_save_file, first_interval=0.1)

    def execute_next(self):
        if self.current_asset_name == "":
            if not self.asset_names:
                message_box(message="Work completed !")
                return
            self.current_asset_name = self.asset_names.pop(0)
            self.current_asset_type = self.asset_types.pop(0)
        new_filepath = os.path.join(self.target_folder, self.current_asset_name + ".blend")
        self.open_or_create_file(new_filepath)

        bpy.app.timers.register(self.append_asset_and_save_file, first_interval=0.1)

    def open_or_create_file(self, filepath=None):
        if filepath is None:
            filepath = self.filepath
        if os.path.isfile(filepath):
            bpy.ops.wm.open_mainfile(filepath=filepath)
        else:
            create_new_file_and_set_as_current(filepath)

    def append_all_assets_and_save_file(self):
        for name, _type in zip(self.asset_names, self.asset_types):
            self.current_asset_name = name
            self.current_asset_type = _type
            if not self.overwrite and item_exists(name, _type):
                continue
            self.append_asset()
        save_file(remove_backup=self.prevent_backup)

    def append_asset_and_save_file(self):
        if self.overwrite or not item_exists(self.current_asset_name, self.current_asset_type):
            self.append_asset()
            save_file(remove_backup=self.prevent_backup)
        self.current_asset_name = ""
        self.current_asset_type = ""
        self.execute_next()

    def append_asset(self):
        bpy.ops.wm.append(
            filepath=os.path.join(self.source_file, self.current_asset_type, self.current_asset_name),
            directory=os.path.join(self.source_file, self.current_asset_type),
            filename=self.current_asset_name,
        )
