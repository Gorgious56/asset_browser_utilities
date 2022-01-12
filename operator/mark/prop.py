from bpy.types import PropertyGroup
from bpy.props import BoolProperty


class OperatorProperties(PropertyGroup):
    overwrite: BoolProperty(
        name="Overwrite assets",
        description="Check to re-mark assets and re-generate preview if the item is already an asset",
        default=False,
    )
    mark: BoolProperty(
        name="Mark",
        description="Check to Mark existing assets rather than unmarking items",
        default=False,
    )
    generate_previews: BoolProperty(
        default=True,
        name="Generate Previews",
        description="When marking assets, automatically generate a preview\nUncheck to mark assets really fast",
    )
    force_previews: BoolProperty(
        default=False,
        name="Re-generate Previews",
        description="Enable to force re-generating previews on all assets without needing to unmark/remark it",
    )

    def draw(self, layout):
        if self.mark:
            layout.prop(self, "overwrite", icon="ASSET_MANAGER")
            row = layout.row(align=True)
            row.prop(self, "generate_previews", icon="RESTRICT_RENDER_OFF")
            row.prop(self, "force_previews", icon="FILE_REFRESH", text="")
