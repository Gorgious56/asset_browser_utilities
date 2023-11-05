from asset_browser_utilities.module.tag.tool import ensure_asset_has_uuid_tag, has_asset_tag_uuid, get_uuid_from_tag


def ensure_asset_uuid(asset):
    tag = ensure_asset_has_uuid_tag(asset)
    return get_uuid_from_tag(tag)


def get_asset_uuid(asset):
    tag = has_asset_tag_uuid(asset)
    return get_uuid_from_tag(tag) if tag else None
