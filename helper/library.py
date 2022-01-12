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
        bpy.ops.ed.lib_id_load_custom_preview(filepath=filepath)
    else:
        bpy.ops.ed.lib_id_load_custom_preview({"id": asset}, filepath=filepath)
