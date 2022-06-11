import bpy
from asset_browser_utilities.module.asset.tool import is_asset


CATALOG_FROM_UUID = "6a287106-5984-4db7-ae6d-b02ff955b0ac"
CATALOG_TO_UUID = "02c809ff-cf34-473b-b348-1eadcdd87472"


def all_assets_in_specific_catalog_container_and_name(uuid):
    asset_names = []
    for d in dir(bpy.data):
        container = getattr(bpy.data, d)
        if "bpy_prop_collection" in str(type(container)):
            for asset in container:
                if is_asset(asset) and asset.asset_data.catalog_id == uuid:
                    asset_names.append((d, asset.name))
    return asset_names


def assert_that_asset_is_in_catalog(asset, uuid):
    assert (
        asset.asset_data.catalog_id == uuid
    ), f"{repr(asset)}'s catalog should be '{uuid}' instead of '{asset.asset_data.catalog_id}'"
