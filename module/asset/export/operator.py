from pathlib import Path
import threading
import queue

import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, PointerProperty, BoolProperty

from asset_browser_utilities.core.cache.tool import get_current_operator_properties, get_from_cache, get_cache
from asset_browser_utilities.core.console import command_execute_on_blend_file, command_line_execute_base
from asset_browser_utilities.core.console.builder import CommandBuilder
from asset_browser_utilities.core.file.save import (
    create_new_file_and_set_as_current,
    save_if_possible_and_necessary,
    sanitize_filepath,
    save_file_as,
    save_file,
)
from asset_browser_utilities.core.file.path import (
    get_folder_from_path,
    open_file_if_different_from_current,
)
from asset_browser_utilities.core.filter.main import AssetFilterSettings
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.library.tool import (
    get_directory_name,
    get_blend_data_name_from_directory,
    append_asset,
)
from asset_browser_utilities.core.library.prop import LibraryExportSettings, LibraryType
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator

from asset_browser_utilities.module.library.link.tool import replace_asset_with_linked_one
from asset_browser_utilities.module.library.tool import ensure_asset_uuid
from asset_browser_utilities.module.catalog.tool import CatalogsHelper

from asset_browser_utilities.module.asset.export.tool import get_exported_asset_filepath


class CommandLineExecute(command_line_execute_base.CommandLineExecuteBase):
    asset_name: str
    asset_directory: str
    asset_filepath: str
    source_file: str
    remove_backup: bool
    overwrite: bool

    def run(self):
        print(get_current_operator_properties())
        append_asset(
            self.attributes["source_file"],
            self.attributes["asset_directory"],
            self.attributes["asset_name"],
            overwrite=self.attributes["overwrite"],
        )
        save_file_as(filepath=self.attributes["asset_filepath"], remove_backup=self.attributes["remove_backup"])
        Logger.display(
            f"Exported Asset '{self.attributes['asset_directory']}/{self.attributes['asset_name']}' to '{self.attributes['asset_filepath']}'"
        )
        quit()


class AssetExportOperatorProperties(PropertyGroup):
    individual_files: BoolProperty(
        name="Place Assets in Individual Files",
        description="If this is ON, each asset will be exported to an individual file in the target directory.\
\nEach asset will be placed in a blend file named after itself\
\nBeware of name collisions",
        default=True,
    )
    catalog_folders: BoolProperty(
        name="Add Folders from Catalogs",
        default=True,
    )
    overwrite: BoolProperty(
        name="Overwrite Assets",
        description="Check to overwrite objects if an object with the same name already exists in target file",
        default=True,
    )
    link_back: BoolProperty(
        name="Link Assets Back",
        description="Remove the assets from current file and link back using the exported file as a library",
        default=False,
    )

    def draw(self, layout, context=None):
        layout.prop(self, "individual_files", icon="NEWFOLDER")
        catalog_folders_row = layout.row()
        catalog_folders_row.prop(self, "catalog_folders", icon="OUTLINER")
        catalog_folders_row.active = self.individual_files
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")
        layout.prop(self, "link_back", icon="LINKED")


class ABU_OT_asset_export(Operator, BatchFolderOperator):
    ui_library = LibraryType.FileCurrent.value
    bl_idname = "abu.asset_export"
    bl_label = "Export Assets"
    bl_description: str = "Export Assets To External File(s)"

    operator_settings: PointerProperty(type=AssetExportOperatorProperties)
    logic_class = BatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True, enforce_filebrowser=True)

    def execute(self, context):
        self.write_filepath_to_cache()
        self.init()
        save_file()
        if len(self.asset_names) > 0:
            self.run()
        else:
            Logger.display("No asset to export")
        return {"FINISHED"}

    def init(self):
        assets = get_from_cache(AssetFilterSettings).get_objects_that_satisfy_filters()
        self.asset_names = [a.name for a in assets]
        self.asset_directories = [get_directory_name(a) for a in assets]
        self.asset_uuids = [ensure_asset_uuid(a) for a in assets]
        if len(self.asset_uuids) != len(set(self.asset_uuids)):
            assert (
                False
            ), "At least two assets share the same UUID. Please regenerate uuids using Add Smart Tag > UUID."
        catalogs_map = {c[0]: c[1] for c in CatalogsHelper.get_catalogs()}
        self.asset_folders = [catalogs_map.get(a.asset_data.catalog_id, "") for a in assets]

    def run(self):
        root_folder = str(get_folder_from_path(self.filepath))
        source_filepath = bpy.data.filepath
        if get_current_operator_properties().individual_files:
            self.run_batch(root_folder, source_filepath)
        else:
            self.run_once(source_filepath)

    def run_batch(self, root_folder, source_filepath):
        current_operator_properties = get_current_operator_properties()
        asset_names_queue = queue.Queue(maxsize=len(self.asset_names))
        for asset_directory in self.asset_names:
            asset_names_queue.put(asset_directory)

        asset_directories_queue = queue.Queue(maxsize=len(self.asset_directories))
        for asset_directory in self.asset_directories:
            asset_directories_queue.put(asset_directory)

        asset_folders_queue = queue.Queue(maxsize=len(self.asset_folders))
        for asset_folder in self.asset_folders:
            asset_folders_queue.put(asset_folder)

        def run():
            print(threading.current_thread().name, " Starting")

            asset_name = asset_names_queue.get()
            asset_directory = asset_directories_queue.get()
            asset_folder = asset_folders_queue.get()
            asset_filepath = str(
                get_exported_asset_filepath(
                    root_folder, asset_folder, asset_name, current_operator_properties.catalog_folders
                )
            )
            asset_filepath = sanitize_filepath(asset_filepath)

            caller = CommandBuilder(
                script_filepath=command_execute_on_blend_file.__file__,
                blend_filepath=asset_filepath if Path(asset_filepath).exists() else None,
            )
            caller.add_arg_value("asset_name", asset_name)
            caller.add_arg_value("asset_directory", asset_directory)
            caller.add_arg_value("asset_filepath", asset_filepath)
            caller.add_arg_value("source_file", source_filepath)
            caller.add_arg_value("remove_backup", get_from_cache(LibraryExportSettings).remove_backup)
            caller.add_arg_value("overwrite", current_operator_properties.overwrite)
            caller.add_arg_value("source_operator_file", __file__)
            caller.call()

            print(threading.current_thread().name, " Exiting")

        threads = [threading.Thread(name="Thread %d" % i, target=run) for i in range(len(self.asset_names))]
        print("Starting threads...")
        for thread in threads:
            thread.start()
        print("Waiting for threads to finish...")
        for thread in threads:
            thread.join()

        if current_operator_properties.link_back:
            for asset_name, asset_directory, asset_folder in zip(
                self.asset_names, self.asset_directories, self.asset_folders
            ):
                link_filepath = get_exported_asset_filepath(
                    str(get_folder_from_path(self.filepath)),
                    asset_folder,
                    asset_name,
                    current_operator_properties.catalog_folders,
                )
                link_filepath = sanitize_filepath(link_filepath)
                blend_data_name = get_blend_data_name_from_directory(asset_directory)
                replace_asset_with_linked_one(
                    getattr(bpy.data, blend_data_name)[asset_name],
                    link_filepath,
                    asset_directory,
                    asset_name,
                    create_liboverrides=False,
                )
                save_if_possible_and_necessary()

    def run_once(self, source_filepath):
        current_operator_properties = get_current_operator_properties()
        target_filepath = sanitize_filepath(self.filepath)
        if Path(target_filepath).exists():
            open_file_if_different_from_current(target_filepath)
        else:
            create_new_file_and_set_as_current(target_filepath)
        for asset_name, asset_directory in zip(self.asset_names, self.asset_directories):
            append_asset(source_filepath, asset_directory, asset_name, overwrite=current_operator_properties.overwrite)
        save_file()
        open_file_if_different_from_current(source_filepath)
        if current_operator_properties.link_back:
            for asset_name, asset_directory in zip(self.asset_names, self.asset_directories):
                blend_data_name = get_blend_data_name_from_directory(asset_directory)
                replace_asset_with_linked_one(
                    getattr(bpy.data, blend_data_name)[asset_name],
                    target_filepath,
                    asset_directory,
                    asset_name,
                    create_liboverrides=False,
                )
                save_if_possible_and_necessary()
