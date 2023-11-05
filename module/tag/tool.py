from bpy.types import PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.core.filter.name import FilterName
from asset_browser_utilities.core.tool import generate_uuid

from asset_browser_utilities.module.tag.prop import ASSET_TAG_UUID_PREFIX, ASSET_TAG_LINK_UUID_PREFIX
from asset_browser_utilities.module.tag.tag_collection import TagCollection

from asset_browser_utilities.core.library.tool import get_directory_name


def get_uuid_from_tag(tag):
    return tag.name.split(":")[-1] if tag else None


def get_asset_tag_uuid_name():
    return f"{ASSET_TAG_UUID_PREFIX}:{generate_uuid()}"


def get_asset_tag_link_uuid_name_from_directory_and_name_and_uuid(directory, name, uuid):
    char_limit = 63 - 3 - len(directory) - len(uuid) - len(ASSET_TAG_LINK_UUID_PREFIX)
    name = name if len(name) < char_limit else name[0:char_limit]
    return f"{ASSET_TAG_LINK_UUID_PREFIX}:{directory}:{name}:{uuid}"


def get_asset_tag_link_uuid_name_from_asset(asset):
    return get_asset_tag_link_uuid_name_from_directory_and_name_and_uuid(
        directory=get_directory_name(asset),
        name=asset.name,
        uuid=get_uuid_from_tag(has_asset_tag_uuid(asset)),
    )


def has_asset_tag_uuid(asset):
    for tag in asset.asset_data.tags:
        if tag.name.startswith(ASSET_TAG_UUID_PREFIX):
            return tag


def has_asset_tag(asset, tag_name):
    for tag in asset.asset_data.tags:
        if tag.name == tag_name:
            return tag


def ensure_asset_has_uuid_tag(asset):
    if tag := has_asset_tag_uuid(asset):
        return tag
    return asset.asset_data.tags.new(get_asset_tag_uuid_name())


def add_asset_tag_link_uuid_from_asset_dummy(asset, linked_asset_dummy):
    tag_link_uuid_name = get_asset_tag_link_uuid_name_from_directory_and_name_and_uuid(
        linked_asset_dummy.directory, linked_asset_dummy.name, linked_asset_dummy.uuid
    )
    asset.asset_data.tags.new(tag_link_uuid_name, skip_if_exists=True)


def add_asset_tag_link_uuid_from_other_asset(asset, linked_asset):
    tag_link_uuid_name = get_asset_tag_link_uuid_name_from_asset(linked_asset)
    asset.asset_data.tags.new(tag_link_uuid_name, skip_if_exists=True)


class TagAddOrRemoveOperatorProperties(PropertyGroup):
    tag_collection: PointerProperty(type=TagCollection)
    MAX_TAGS = 10
    filter_name: PointerProperty(type=FilterName)

    def init(self, add=True):
        self.tag_collection.add = add
        self.tag_collection.init(tags=self.MAX_TAGS)

    def draw(self, layout, context=None):
        box = layout.box()
        self.tag_collection.draw(box)
        if self.tag_collection.remove_all:
            self.filter_name.draw(box)

    @property
    def tags(self):
        return [t.name for t in self.tag_collection.items if not t.is_empty()]
