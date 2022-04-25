import bpy  # Do not remove even if it seems unused !!
from asset_browser_utilities.core.cache.tool import CacheMapping
from asset_browser_utilities.transform.operation import TransformApplyOperation as TransformApply
from bpy.types import PropertyGroup
from bpy.props import EnumProperty, BoolProperty

OPERATION_MAPPING = {
    TransformApply.MAPPING: TransformApply,
}


class OperationSettings(PropertyGroup, CacheMapping):
    CACHE_MAPPING = "operation_settings"

    active: BoolProperty(default=False)
    operation: EnumProperty(
        name="Operation",
        items=((TransformApply.MAPPING, TransformApply.LABEL, TransformApply.DESCRIPTION),),
    )

    def draw(self, layout, context):
        box = layout.box()
        box.prop(self, "active", text="Additional Operations", toggle=True, icon="MODIFIER")
        if self.active:
            box.prop(self, "operation")

    def execute(self, assets):
        if not self.active:
            return
        operation_cls = OPERATION_MAPPING.get(self.operation)
        if not operation_cls:
            return
        operator = f"bpy.ops.{operation_cls.OPERATION}({{'{operation_cls.ATTRIBUTE}': assets}})"
        exec(operator)
