from bpy.types import PropertyGroup
from bpy.props import BoolProperty


class FilterSelection(PropertyGroup):
    active: BoolProperty(
        default=False, name="Filter By Selection", description="Filter items by selection when applicable"
    )
    allow: BoolProperty(default=False)
    allow_view_3d: BoolProperty(default=True)
    view_3d: BoolProperty(name="3D Viewport", default=False)

    allow_asset_browser: BoolProperty(default=True)
    asset_browser: BoolProperty(name="Asset Browser", default=True)

    def init(self, allow):
        self.allow = allow

    def draw(self, layout, context=None):
        if self.allow:
            box = layout.box()
            box.prop(self, "active", icon="RESTRICT_SELECT_OFF")
            if self.active:
                column = box.column(align=True)
                column.prop(self, "view_3d", toggle=True, icon="VIEW3D")
                if self.allow_asset_browser:
                    column.prop(self, "asset_browser", toggle=True, icon="ASSET_MANAGER")
