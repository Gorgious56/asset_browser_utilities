from pathlib import Path

import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, PointerProperty, BoolProperty, CollectionProperty, StringProperty

from asset_browser_utilities.core.cache.tool import get_current_operator_properties, get_from_cache
from asset_browser_utilities.core.file.save import (
    sanitize_filepath,
    save_file_as,
    save_if_file_exists_and_is_dirty,
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
from asset_browser_utilities.core.operator.tool import BatchFolderOperator

from asset_browser_utilities.module.library.tool import ensure_asset_uuid
from asset_browser_utilities.module.catalog.tool import CatalogsHelper
from asset_browser_utilities.module.asset.export.tool import get_exported_asset_filepath
from asset_browser_utilities.module.library.link.prop import AssetDummy
from asset_browser_utilities.module.library.link.tool import replace_asset_with_linked_one


class AssetExportPropertyGroup(PropertyGroup):
    filepath: StringProperty()
    assets: CollectionProperty(type=AssetDummy)


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
    file_exports: CollectionProperty(type=AssetExportPropertyGroup)
    source_filepath: StringProperty()
    export_root_folder: StringProperty()
    export_filepath: StringProperty()

    def draw(self, layout, context=None):
        layout.prop(self, "individual_files", icon="NEWFOLDER")
        catalog_folders_row = layout.row()
        catalog_folders_row.prop(self, "catalog_folders", icon="OUTLINER")
        catalog_folders_row.active = self.individual_files
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")
        layout.prop(self, "link_back", icon="LINKED")

    def ensure_asset_uuids_are_unique(self):
        uuids = []
        for asset in get_from_cache(AssetFilterSettings).get_objects_that_satisfy_filters():
            asset_uuid = ensure_asset_uuid(asset)
            if asset_uuid in uuids:
                assert (
                    False
                ), "At least two assets share the same UUID. Please regenerate uuids using Add Smart Tag > UUID."
            uuids.append(asset_uuid)

    def init_before_exec(self):
        self.source_filepath = bpy.data.filepath
        assets = get_from_cache(AssetFilterSettings).get_objects_that_satisfy_filters()
        self.file_exports.clear()
        catalogs_map = {c[0]: c[1] for c in CatalogsHelper.get_catalogs()}
        self.ensure_asset_uuids_are_unique()
        if self.individual_files:
            file_export_filepaths = {}
            for asset in assets:
                asset_filepath = str(
                    get_exported_asset_filepath(
                        self.export_root_folder,
                        catalogs_map.get(asset.asset_data.catalog_id, ""),
                        asset.name,
                        self.catalog_folders,
                    )
                )
                asset_filepath = sanitize_filepath(asset_filepath)
                if asset_filepath in file_export_filepaths.keys():
                    file_export = file_export_filepaths[asset_filepath]
                else:
                    file_export = self.file_exports.add()
                    file_export.filepath = asset_filepath
                    file_export_filepaths[asset_filepath] = file_export
                new_asset = file_export.assets.add()
                new_asset.name = asset.name
                new_asset.directory = get_directory_name(asset)
                new_asset.uuid = ensure_asset_uuid(asset)
        else:
            file_export = self.file_exports.add()
            file_export.filepath = self.export_filepath
            for asset in assets:
                new_asset = file_export.assets.add()
                new_asset.name = asset.name
                new_asset.directory = get_directory_name(asset)
                new_asset.uuid = ensure_asset_uuid(asset)

    def run_in_file(self, attributes=None):
        file_export = self.file_exports[int(attributes["thread_index"])]
        if Path(file_export.filepath).exists():
            open_file_if_different_from_current(file_export.filepath)
        for asset_dummy in file_export.assets:
            asset = append_asset(
                self.source_filepath,
                asset_dummy.directory,
                asset_dummy.name,
                overwrite=self.overwrite,
            )
            Logger.display(f"Exported Asset '{repr(asset)}' to '{file_export.filepath}'")
        save_file_as(
            filepath=file_export.filepath,
            remove_backup=get_from_cache(LibraryExportSettings).remove_backup,
        )
        return False


class ABU_OT_asset_export(Operator, BatchFolderOperator):
    ui_library = LibraryType.FileCurrent.value
    bl_idname = "abu.asset_export"
    bl_label = "Export Assets"
    bl_description: str = "Export Assets To External File(s)"
    filepath:StringProperty()

    operator_settings: PointerProperty(type=AssetExportOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True, enforce_filebrowser=True)

    def init_after_invoke_but_before_execute(self):
        op_props = get_current_operator_properties()
        op_props.export_filepath = self.filepath
        op_props.export_root_folder = str(get_folder_from_path(self.filepath))
        op_props.init_before_exec()

    def execute(self, context):
        self.init_after_invoke_but_before_execute()
        bpy.ops.wm.save_userpref()
        self.run_in_threads(context)
        context.window_manager.event_timer_add(time_step=0.1, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def filter_files(self, files):
        return [None] * len(get_current_operator_properties().file_exports)

    def on_finish(self):
        op_props = get_current_operator_properties()
        if op_props.link_back:
            for file_export in op_props.file_exports:
                for asset in file_export.assets:
                    blend_data_name = get_blend_data_name_from_directory(asset.directory)
                    replace_asset_with_linked_one(
                        getattr(bpy.data, blend_data_name)[asset.name],
                        file_export.filepath,
                        asset.directory,
                        asset.name,
                        create_liboverrides=False,
                    )
            save_if_file_exists_and_is_dirty()
