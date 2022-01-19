from asset_browser_utilities.file.path import is_this_current_file
import bpy


CONTAINERS = (
    "actions",
    "materials",
    "objects",
    "worlds",
)


def item_exists(name, _type):
    library = getattr(bpy.data, _type.lower() + "s")
    return library.get(name) is not None


def get_all_assets_in_file():
    assets = []
    for container in CONTAINERS:
        assets.extend([a for a in getattr(bpy.data, container) if a.asset_data])
    return assets


def generate_asset_preview(filepath, asset=None):
    if asset is None:
        bpy.ops.ed.lib_id_load_custom_preview(filepath=str(filepath))
    else:
        bpy.ops.ed.lib_id_load_custom_preview({"id": asset}, filepath=str(filepath))


def get_blend_library_name(asset):
    return type(asset).__name__.lower() + "s"


def append_asset(filepath, directory, filename):
    if is_this_current_file(filepath):
        return
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
