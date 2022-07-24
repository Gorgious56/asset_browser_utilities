from pathlib import Path
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.file.path import is_this_current_file
import bpy


def item_exists(name, _type):
    library = getattr(bpy.data, _type.lower() + "s")
    return library.get(name) is not None


def load_preview(filepath, asset=None):
    if asset is None:
        bpy.ops.ed.lib_id_load_custom_preview(filepath=str(filepath))
    else:
        if bpy.app.version >= (3, 2, 0):
            with bpy.context.temp_override(id=asset):
                bpy.ops.ed.lib_id_load_custom_preview(filepath=str(filepath))
        else:
            bpy.ops.ed.lib_id_load_custom_preview({"id": asset}, filepath=str(filepath))
    Logger.display(f"Loaded custom preview from '{filepath}' for asset '{asset.name or 'active asset'}'")


def get_blend_library_name(asset):
    return type(asset).__name__.lower() + "s"


def get_blend_files_in_folder(folder, recursive):
    if isinstance(folder, str):
        folder = Path(folder)
    if recursive:
        return [fp for fp in folder.glob("**/*.blend") if fp.is_file()]
    else:
        return [fp for fp in folder.glob("*.blend") if fp.is_file()]


def sanitize_library_name(name):
    if name == "geometrynodetrees" or name == "nodetrees":
        name = "node_groups"
    elif name == "brushs":
        name = "brushes"
    elif "texture" in name:
        name = "textures"
    if name.endswith("ss"):
        name = name[0:-1]
    return name


def append_asset(filepath, directory, filename):
    if is_this_current_file(filepath):
        return
    directory = sanitize_library_name(directory)
    # https://blender.stackexchange.com/a/33998/86891
    library = getattr(bpy.data, directory)
    with bpy.data.libraries.load(str(filepath)) as (data_from, data_to):
        other_asset = library.get(filename)
        if other_asset is not None:  # If we don't change existing asset with same name, we can't append a new one.
            other_asset.name = "__ABU_TEMP_FOR_APPENDING_"
        library_to = getattr(data_to, directory)
        library_to.append(filename)

    obj = library.get(filename)
    if obj:
        if directory == "objects":
            bpy.context.scene.collection.objects.link(obj)
        else:
            obj.use_fake_user = True
    if other_asset is not None:
        other_asset.name = filename


def iterate_over_all_containers():
    for d in dir(bpy.data):
        container = getattr(bpy.data, d)
        if "bpy_prop_collection" in str(type(container)):
            for asset in container:
                yield asset
