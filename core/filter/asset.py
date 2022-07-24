from bpy.types import PropertyGroup
from bpy.props import BoolProperty


class FilterAssets(PropertyGroup):
    active: BoolProperty(default=True, name="Filter Assets")
    allow: BoolProperty(default=True)
    optional: BoolProperty(default=False)

    def draw(self, layout):
        if self.allow and self.optional:
            box = layout.box()
            box.prop(self, "active", icon="FILTER")
