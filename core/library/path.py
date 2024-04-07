from pathlib import Path
import bpy


def get_library_root(context, library_name=None):
    if library_name is None:
        library_name = context.area.spaces.active.params.asset_library_reference
    if library_name == "LOCAL":  # Current file
        library_path = Path(bpy.data.filepath)  # Will be "" if file has never been saved
        if library_path:
            library_path = library_path.parent
    else:
        library_path = Path(context.preferences.filepaths.asset_libraries.get(library_name).path)

    return library_path


def get_asset_filepath(context, asset):
    current_library_name = context.area.spaces.active.params.asset_library_reference
    for asset_file in context.selected_assets:
        if asset_file.asset_data == asset.asset_data:
            asset_fullpath = asset_file.full_library_path
            if current_library_name == "LOCAL":
                asset_fullpath /= asset_file.local_id.name
            asset_filepath = asset_fullpath.parent.parent
            return asset_filepath
