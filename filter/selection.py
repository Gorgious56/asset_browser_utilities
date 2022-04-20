from bpy.types import PropertyGroup
from bpy.props import EnumProperty, BoolProperty


class Sources:
    VIEW_3D = "VIEW_3D"
    ASSET_BROWSER = "ASSETS"
    OUTLINER = "OUTLINER"


class FilterSelection(PropertyGroup):
    source: EnumProperty(
        items=(
            (
                Sources.VIEW_3D,
                "3D Viewport",
                "Filter Selection from the currently selected objects in the viewport",
                "VIEW3D",
                1,
            ),
            (
                Sources.ASSET_BROWSER,
                "Asset Browser",
                "Filter Selection from the currently selected assets in the asset browser",
                "ASSET_MANAGER",
                2,
            ),
            (
                Sources.OUTLINER,
                "Outliner",
                "Filter Selection from the currently selected items in the outliner",
                "OUTLINER",
                3,
            ),
        ),
        default=Sources.ASSET_BROWSER,
    )
    active: BoolProperty(
        default=False, name="Filter By Selection", description="Filter items by selection when applicable"
    )
    allow: BoolProperty(default=False)

    def draw(self, layout):
        if self.allow:
            box = layout.box()
            box.prop(self, "active", icon="RESTRICT_SELECT_OFF")
            row = box.row(align=True)
            if self.active:
                row.props_enum(self, "source")
