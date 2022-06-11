import bpy


def ensure_object_is_not_asset(obj):
    obj.asset_clear()


def is_asset(obj):
    return obj.asset_data is not None


def all_assets():
    for d in dir(bpy.data):
        container = getattr(bpy.data, d)
        if "bpy_prop_collection" in str(type(container)):
            for asset in container:
                if is_asset(asset):
                    yield asset


def all_assets_container_and_name():
    asset_names = []
    for d in dir(bpy.data):
        container = getattr(bpy.data, d)
        if "bpy_prop_collection" in str(type(container)):
            for asset in container:
                if is_asset(asset):
                    asset_names.append((d, asset.name))
    return asset_names
