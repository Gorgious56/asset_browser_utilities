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

    def init(self, allow, allow_view_3d=True, allow_asset_browser=True):
        self.allow = allow
        self.allow_view_3d = allow_view_3d
        self.allow_asset_browser = allow_asset_browser

    def draw(self, layout, context=None):
        if self.allow and (self.allow_view_3d or self.allow_asset_browser):
            box = layout.box()
            box.prop(self, "active", icon="RESTRICT_SELECT_OFF")
            if self.active:
                column = box.column(align=True)
                if self.allow_view_3d:
                    column.prop(self, "view_3d", toggle=True, icon="VIEW3D")
                if self.allow_asset_browser:
                    column.prop(self, "asset_browser", toggle=True, icon="ASSET_MANAGER")
