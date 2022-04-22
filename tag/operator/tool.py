from bpy.types import PropertyGroup
from bpy.props import PointerProperty

from asset_browser_utilities.tag.tag_collection import TagCollection


class AddOrRemoveTagsOperatorProperties(PropertyGroup):
    tag_collection: PointerProperty(type=TagCollection)
    MAX_TAGS = 10

    def init(self, add=True):
        self.tag_collection.add = add
        self.tag_collection.init(tags=self.MAX_TAGS)

    def draw(self, layout):
        self.tag_collection.draw(layout)
