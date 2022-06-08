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
    case_sensitive: BoolProperty(default=True, name="Case sensitive")

    def draw(self, layout, name_override=""):
        box = layout.box()
        label = "Filter " + (f"{name_override} " if name_override != "" else "") + "By Name"
        box.prop(self, "active", text=label, icon="FILTER")
        if self.active:
            box.prop(self, "value", text="Text")
            box.prop(self, "case_sensitive")
            row = box.row(align=True)
            row.props_enum(self, "method")

    def filter(self, test):
        return FilterName.filter_static(test, self.method, self.value, self.case_sensitive)

    @staticmethod
    def filter_static(test, method, value, case_sensitive):
        if not case_sensitive:
            test = test.lower()
            value = value.lower()
        if method == "Prefix":
            return test.startswith(value)
        elif method == "Contains":
            return value in test
        elif method == "Suffix":
            return test.endswith(value)
