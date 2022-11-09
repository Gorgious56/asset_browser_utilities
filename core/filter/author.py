from bpy.types import PropertyGroup
from bpy.props import StringProperty, BoolProperty


class FilterAuthor(PropertyGroup):
    active: BoolProperty(default=False)
    name: StringProperty(name="Name", default="")

    def init(self):
        self.tags.init()
        self.tags.add = True

    def draw(self, layout, context=None):
        box = layout.box()
        box.prop(self, "active", icon="FILTER", text="Filter by Author")
        if self.active:
            box.prop(self, "name")
