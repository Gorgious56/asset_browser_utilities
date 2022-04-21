from pathlib import Path
import bpy


def get_library_root(context, library_name=None):
    if library_name is None:
        library_name = context.area.spaces.active.params.asset_library_ref
    if library_name == "LOCAL":  # Current file
        library_path = Path(bpy.data.filepath)  # Will be "" if file has never been saved
        if library_path:
            library_path = library_path.parent
    else:
        library_path = Path(context.preferences.filepaths.asset_libraries.get(library_name).path)

    return library_path
