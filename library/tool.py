from asset_browser_utilities.file.path import is_this_current_file
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


def get_blend_library_name(asset):
    return type(asset).__name__.lower() + "s"


def get_blend_files_in_folder(folder, recursive):
    if recursive:
        return [fp for fp in folder.glob("**/*.blend") if fp.is_file()]
    else:
        return [fp for fp in folder.glob("*.blend") if fp.is_file()]


def append_asset(filepath, directory, filename):
    if is_this_current_file(filepath):
        return
    if directory == "geometrynodetrees":
        directory = "node_groups"
    elif directory == "brushs":
        directory = "brushes"
    elif "texture" in directory:
        directory = "textures"
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
