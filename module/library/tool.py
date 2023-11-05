from asset_browser_utilities.module.tag.tool import ensure_asset_has_uuid_tag


def ensure_asset_uuid(asset):
    tag = ensure_asset_has_uuid_tag(asset)
    return tag.name.split(":")[1]
