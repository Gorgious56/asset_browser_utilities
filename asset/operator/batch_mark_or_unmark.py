import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty

from asset_browser_utilities.library.operator import BatchOperator
from asset_browser_utilities.library.execute import BatchExecute


class BatchUnmark(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        if self.assets:
            for asset in self.assets:
                asset.asset_clear()
            self.save_file()
        self.execute_next_blend()


class BatchMark(BatchExecute):
    def execute_one_file_and_the_next_when_finished(self):
        if not self.assets:
            self.execute_next_blend()
            return

        for asset in self.assets:
            if asset.asset_data and not self.overwrite:
                continue
            asset.asset_mark()
            asset.asset_generate_preview()

        if self.generate_previews:
            bpy.app.timers.register(self.sleep_until_previews_are_done_and_execute_next_file)
        else:
            self.save_file()
            self.execute_next_blend()


class OperatorPropertiesMark(PropertyGroup):
    overwrite: BoolProperty(
        name="Overwrite assets",
        description="Check to re-mark assets and re-generate preview if the item is already an asset",
        default=False,
    )
    generate_previews: BoolProperty(
        default=True,
        name="Generate Previews",
        description="When marking assets, automatically generate a preview\nUncheck to mark assets really fast",
    )

    def draw(self, layout):
        layout.prop(self, "overwrite", icon="ASSET_MANAGER")
        row = layout.row(align=True)
        row.prop(self, "generate_previews", icon="RESTRICT_RENDER_OFF")


class ASSET_OT_batch_mark(Operator, ImportHelper, BatchOperator):
    "Batch Mark Assets"
    bl_idname = "asset.batch_mark"
    bl_label = "Batch Mark Assets"

    operator_settings: PointerProperty(type=OperatorPropertiesMark)
    logic_class = BatchMark

    def invoke(self, context, event):
        self.operator_settings.mark = True
        return self._invoke(context)


class ASSET_OT_batch_unmark(Operator, ImportHelper, BatchOperator):
    "Batch Unmark Assets"
    bl_idname = "asset.batch_unmark"
    bl_label = "Batch Unmark Assets"

    logic_class = BatchUnmark

    def invoke(self, context, event):
        self.operator_settings.mark = False
        return self._invoke(context, filter_assets=True)
