import os.path
from pathlib import Path
import bpy
from asset_browser_utilities.library.helper import item_exists
from asset_browser_utilities.file.path import (
    create_new_file_and_set_as_current,
    save_file,
)
from asset_browser_utilities.core.ui.message import message_box


class BatchExecute:
    def __init__(
        self, asset_names, asset_types, source_file, target_filepath, remove_backup, overwrite, individual_files
    ):
        self.asset_names = asset_names
        self.asset_types = asset_types
        self.current_asset_name = ""
        self.current_asset_type = ""

        self.source_file = Path(str(source_file))
        self.filepath = target_filepath
        self.target_folder = Path(self.filepath).parent

        self.remove_backup = remove_backup
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
        new_filepath = self.target_folder / (self.current_asset_name + ".blend")
        self.open_or_create_file(new_filepath)

        bpy.app.timers.register(self.append_asset_and_save_file_and_execute_next, first_interval=0.1)

    def open_or_create_file(self, filepath=None):
        if filepath is None:
            filepath = self.filepath
        if os.path.isfile(filepath):
            bpy.ops.wm.open_mainfile(filepath=str(filepath))
        else:
            create_new_file_and_set_as_current(str(filepath))

    def append_all_assets_and_save_file(self):
        for name, _type in zip(self.asset_names, self.asset_types):
            self.current_asset_name = name
            self.current_asset_type = _type
            if not self.overwrite and item_exists(name, _type):
                continue
            self.append_asset()
        save_file(remove_backup=self.remove_backup)

    def append_asset_and_save_file_and_execute_next(self):
        if self.overwrite or not item_exists(self.current_asset_name, self.current_asset_type):
            self.append_asset()
            save_file(remove_backup=self.remove_backup)
        self.current_asset_name = ""
        self.current_asset_type = ""
        self.execute_next()

    def append_asset(self):
        # https://blender.stackexchange.com/a/33998/86891
        with bpy.data.libraries.load(str(self.source_file)) as (data_from, data_to):
            library_to = getattr(data_to, self.current_asset_type)
            library_to.append(self.current_asset_name)
        library = getattr(bpy.data, self.current_asset_type)
        obj = library.get(self.current_asset_name)
        if self.current_asset_type == "objects":
            bpy.context.scene.collection.objects.link(obj)
        else:
            obj.use_fake_user = True
