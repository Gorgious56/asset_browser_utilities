from bpy.types import PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.module.tag.tag_collection import TagCollection
from asset_browser_utilities.core.filter.name import FilterName


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
