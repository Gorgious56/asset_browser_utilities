import bpy  # Do not remove even if it seems unused !!
from bpy.types import PropertyGroup
from bpy.props import EnumProperty, BoolProperty, FloatVectorProperty
from asset_browser_utilities.core.cache.tool import CacheMapping
from asset_browser_utilities.transform.operation import (
    ApplyTransformOperation,
    ApplyLocationOperation,
    ApplyScaleOperation,
    ApplyRotationOperation,
    TranslateOperation,
    ScaleOperation,
)


OPERATION_MAPPING = {
    ApplyTransformOperation.MAPPING: ApplyTransformOperation,
    ApplyLocationOperation.MAPPING: ApplyLocationOperation,
    ApplyRotationOperation.MAPPING: ApplyRotationOperation,
    ApplyScaleOperation.MAPPING: ApplyScaleOperation,
    TranslateOperation.MAPPING: TranslateOperation,
    ScaleOperation.MAPPING: ScaleOperation,
}


class OperationSettings(PropertyGroup, CacheMapping):
    CACHE_MAPPING = "operation_settings"

    active: BoolProperty(default=False)
    operation: EnumProperty(
        name="Operation",
        items=[(op.MAPPING, op.LABEL, op.DESCRIPTION) for op in OPERATION_MAPPING.values()],
    )
    vector_value: FloatVectorProperty(name="Value")

    def draw(self, layout, context):
        box = layout.box()
        box.prop(self, "active", text="Custom Operation", toggle=True, icon="MODIFIER")
        if self.active:
            box.prop(self, "operation")
            operation_cls = OPERATION_MAPPING.get(self.operation)
            if operation_cls and not operation_cls.OPERATOR:
                box.prop(self, operation_cls.ATTRIBUTE)

    def execute(self, assets):
        if not self.active:
            return
        operation_cls = OPERATION_MAPPING.get(self.operation)
        if not operation_cls:
            return
        if operation_cls.OPERATOR:
            operation = f"bpy.ops.{operation_cls.OPERATION}({{'{operation_cls.ATTRIBUTE}': assets}}, {operation_cls.ADDITIONAL_ATTRIBUTES})"
            exec(operation)
        else:
            value = getattr(self, operation_cls.ATTRIBUTE)
            operation_cls.OPERATION(assets, value)
