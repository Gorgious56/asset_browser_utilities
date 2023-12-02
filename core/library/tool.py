from pathlib import Path

import bpy

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.file.path import is_this_current_file


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


def get_id_from_file_select(file_select):
    directory, name = get_directory_and_name_from_file_select(file_select)
    blend_data_name = get_blend_data_name_from_directory(directory)
    blend_data = getattr(bpy.data, blend_data_name)
    return blend_data.get(name)


def get_directory_and_name_from_file_select(file_select):
    directory = file_select.relative_path.split("\\")[0]
    name = file_select.relative_path[len(directory) + 1 : :]
    return directory, name


def get_directory_name(asset):
    name = type(asset).__name__.lower()
    if "nodetree" in name:
        name = "nodetree"
    elif "texture" in name:
        name = "texture"
    return name


def sanititize_blend_data_name(name):
    if "nodetree" in name:
        name = "node_groups"
    elif name == "brushs":
        name = "brushes"
    elif "texture" in name:
        name = "textures"
    elif "freestyle" in name:
        name = "linestyles"
    elif "mesh" in name:
        name = "meshes"
    return name


def get_blend_data_name_from_directory(directory):
    name = directory.lower() + "s"
    return sanititize_blend_data_name(name)


def get_blend_data_name(asset):
    name = type(asset).__name__.lower() + "s"
    return sanititize_blend_data_name(name)


def get_files_in_folder(folder, recursive, extension="blend"):
    if isinstance(folder, str):
        folder = Path(folder)
    if recursive:
        return [fp for fp in folder.glob("**/*." + extension) if fp.is_file()]
    else:
        return [fp for fp in folder.glob("*." + extension) if fp.is_file()]


def sanitize_library_name(name):
    if "nodetree" in name:
        name = "node_groups"
    elif name == "brushs":
        name = "brushes"
    elif "texture" in name:
        name = "textures"
    if name.endswith("ss"):
        name = name[0:-1]
    return name


def link_asset(filepath, directory, filename, relative=False, create_liboverrides=False, overwrite=True):
    return append_asset(
        filepath,
        directory,
        filename,
        link=True,
        relative=relative,
        create_liboverrides=create_liboverrides,
        overwrite=overwrite,
    )


def append_asset(
    filepath,
    directory,
    asset_name,
    link=False,
    relative=False,
    create_liboverrides=False,
    overwrite=True,
):
    if is_this_current_file(filepath):
        return
    blend_data_name = get_blend_data_name_from_directory(directory)
    # https://blender.stackexchange.com/a/33998/86891
    library = getattr(bpy.data, blend_data_name)
    with bpy.data.libraries.load(
        str(filepath), link=link, relative=relative, create_liboverrides=create_liboverrides
    ) as (data_from, data_to):
        if not link:
            already_existing_asset = library.get(asset_name)
            if already_existing_asset is not None:  # If we don't change existing asset with same name, we can't append a new one.
                already_existing_asset.name = "__ABU_TEMP_FOR_APPENDING_"
            if overwrite:
                library_to = getattr(data_to, blend_data_name)
                library_to.append(asset_name)
        else:
            library_to = getattr(data_to, blend_data_name)
            library_to.append(asset_name)

    asset = library[asset_name, str(filepath)] if link else library.get(asset_name)
    if asset:
        if blend_data_name == "objects" and asset.name not in bpy.context.scene.collection.all_objects:
            bpy.context.scene.collection.objects.link(asset)
        elif blend_data_name == "collections" and asset.name not in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.link(asset)
        else:
            asset.use_fake_user = True
    if not link and already_existing_asset is not None and overwrite:
        # already_existing_asset.name = asset_name
        if hasattr(library, "remove"):
            library.remove(already_existing_asset)
        else:
            print(repr(already_existing_asset))
    return asset


def iterate_over_all_containers():
    for d in dir(bpy.data):
        container = getattr(bpy.data, d)
        if "bpy_prop_collection" in str(type(container)):
            for asset in container:
                yield asset
