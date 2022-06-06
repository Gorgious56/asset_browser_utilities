import bpy


def ensure_object_is_not_asset(obj):
    obj.asset_clear()


def is_asset(obj):
    return obj.asset_data is not None


def all_assets():
    return [o for o in bpy.data.objects if is_asset(o)]
