from bpy.types import PropertyGroup
from bpy.props import BoolProperty, EnumProperty


class FilterSelection(PropertyGroup):
    active: BoolProperty(
        default=False,
        name="Filter By Selection",
        description="Filter items by selection when applicable",
    )
    allow: BoolProperty(default=False)
    selection_type: EnumProperty(
        default="Asset Browser",
        items=(
            ("Asset Browser",) * 3,
            ("3D Viewport",) * 3,
        ),
    )
    allow_view_3d: BoolProperty(default=True)
    allow_asset_browser: BoolProperty(default=True)

    def init(self, allow, allow_view_3d=True, allow_asset_browser=True):
        self.allow = allow
        self.allow_view_3d = allow_view_3d
        self.allow_asset_browser = allow_asset_browser

    def draw(self, layout, context=None):
        if self.allow:
            box = layout.box()
            box.prop(self, "active", icon="RESTRICT_SELECT_OFF")
            if self.active:
                column = box.column(align=True)
                if self.allow_asset_browser:
                    column.prop_enum(self, "selection_type", "Asset Browser")
                if self.allow_view_3d:
                    column.prop_enum(self, "selection_type", "3D Viewport")
