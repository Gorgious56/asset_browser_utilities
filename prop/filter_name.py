from bpy.types import PropertyGroup
from bpy.props import EnumProperty, StringProperty, BoolProperty


class FilterName(PropertyGroup):
    active: BoolProperty(default=False)

    method: EnumProperty(
        name="Filter Name By",
        items=(
            ("Prefix",) * 3,
            ("Contains",) * 3,
            ("Suffix",) * 3,
        ),
        default="Contains",
    )

    value: StringProperty(name="Name Filter Value", description="Filter assets by name\nLeave empty for no filter")
    
    def draw(self, layout):        
        box = layout.box()
        box.prop(self, "active", text="Filter By Name", icon="FILTER", toggle=False)
        if self.active:        
            box.prop(self, "value", text="Text")
            row = box.row(align=True)
            row.props_enum(self, "method")
    
    def filter(self, items):
        if self.active:
            for i in range(len(items) - 1, -1, -1):
                name = items[i].name
                if self.method == "Prefix":
                    if not name.startswith(self.value):
                        items.pop(i)
                elif self.method == "Contains":
                    if self.value not in name:
                        items.pop(i)
                elif self.method == "Suffix":
                    if not name.endswith(self.value):
                        items.pop(i)
