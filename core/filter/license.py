from bpy.types import PropertyGroup
from bpy.props import StringProperty, BoolProperty


class FilterLicense(PropertyGroup):
    active: BoolProperty(default=False)  # type: ignore
    name: StringProperty(name="Name", default="")  # type: ignore

    def draw(self, layout, context=None):
        box = layout.box()
        box.prop(self, "active", icon="FILTER", text="Filter by License")
        if self.active:
            box.prop(self, "name")
