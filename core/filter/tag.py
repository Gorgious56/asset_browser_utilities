from bpy.types import PropertyGroup
from bpy.props import PointerProperty, BoolProperty, EnumProperty
from asset_browser_utilities.module.tag.tag_collection import TagCollection


class FilterTag(PropertyGroup):
    active: BoolProperty()
    max_tags = 10

    orand: EnumProperty(
        items=[
            ("AND", "Assets must have all the tags", ""),
            ("OR", "Assets must have at least one of the tags", ""),
        ],
        default="AND",
    )
    tags: PointerProperty(type=TagCollection)

    def init(self):
        self.tags.init()
        self.tags.add = True

    def draw(self, layout, context=None):
        box = layout.box()
        box.prop(self, "active", icon="FILTER", text="Filter by Tags")
        if self.active:
            box.prop(self, "orand", expand=True)
            self.tags.draw(box, context)
