from bpy.types import PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.core.filter.name import FilterName
from asset_browser_utilities.core.tool import generate_uuid
from asset_browser_utilities.core.operator.tool import BaseOperatorProps
from asset_browser_utilities.core.log.logger import Logger

from asset_browser_utilities.module.tag.prop import ASSET_TAG_UUID_PREFIX
from asset_browser_utilities.module.tag.tag_collection import TagCollection


def get_uuid_from_tag(tag):
    return tag.name.split(":")[-1] if tag else None


def get_asset_tag_uuid_name():
    return f"{ASSET_TAG_UUID_PREFIX}:{generate_uuid()}"


def has_asset_tag_uuid(asset):
    for tag in asset.asset_data.tags:
        if tag.name.startswith(ASSET_TAG_UUID_PREFIX):
            return tag


def has_asset_tag(asset, tag_name):
    for tag in asset.asset_data.tags:
        if tag.name == tag_name:
            return tag


def set_new_asset_uuid_tag(asset):
    return asset.asset_data.tags.new(get_asset_tag_uuid_name())


def ensure_asset_has_uuid_tag(asset):
    if tag := has_asset_tag_uuid(asset):
        return tag
    return set_new_asset_uuid_tag(asset)


class TagAddOrRemoveOperatorProperties(PropertyGroup, BaseOperatorProps):
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

    def run_on_asset(self, asset):
        if self.tag_collection.add:
            asset_data = asset.asset_data
            asset_tags = asset_data.tags
            for tag in self.tags:
                asset_tags.new(tag, skip_if_exists=True)
                Logger.display(f"Added tag '{tag}' to {asset.name}")
        else:
            asset_data = asset.asset_data
            asset_tags = asset_data.tags
            self.execute_tags(asset_tags)

    def execute_tags(self, asset_tags):
        if self.tag_collection.remove_all:
            if self.filter_name.active:
                tags_to_remove = [
                    t.name
                    for t in asset_tags
                    if FilterName.filter_static(
                        t.name,
                        self.filter_name.method,
                        self.filter_name.value,
                        self.filter_name.case_sensitive,
                    )
                ]
                self.remove_tags(asset_tags, tags_to_remove)
            else:
                while asset_tags:
                    asset_tags.remove(asset_tags[0])
                Logger.display(f"Removed all tags from {asset_tags.id_data.name}")
        else:
            self.remove_tags(asset_tags, self.tags)

    def remove_tags(self, asset_tags, tags_to_remove):
        for i in range(len(asset_tags) - 1, -1, -1):
            if asset_tags[i].name in tags_to_remove:
                asset_tags.remove(asset_tags[i])
        Logger.display(f"Removed tags '{tags_to_remove}' from {asset_tags.id_data.name}")
