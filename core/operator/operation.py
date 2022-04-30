from asset_browser_utilities.core.helper import copy_simple_property_group
import bpy  # Do not remove even if it seems unused !!
from bpy.types import PropertyGroup
from bpy.props import EnumProperty, BoolProperty, FloatVectorProperty, CollectionProperty, IntProperty
from asset_browser_utilities.core.cache.tool import CacheMapping
from asset_browser_utilities.transform.operation import (
    ApplyTransformOperation,
    ApplyLocationOperation,
    ApplyScaleOperation,
    ApplyRotationOperation,
    TranslateOperation,
    ScaleOperation,
    RotateOperation,
)


class NONE_OPERATION:
    MAPPING = "NONE"
    LABEL = "None"
    DESCRIPTION = "No Operation"


OPERATION_MAPPING = {
    NONE_OPERATION.MAPPING: NONE_OPERATION,
    ApplyTransformOperation.MAPPING: ApplyTransformOperation,
    ApplyLocationOperation.MAPPING: ApplyLocationOperation,
    ApplyRotationOperation.MAPPING: ApplyRotationOperation,
    ApplyScaleOperation.MAPPING: ApplyScaleOperation,
    TranslateOperation.MAPPING: TranslateOperation,
    ScaleOperation.MAPPING: ScaleOperation,
    RotateOperation.MAPPING: RotateOperation,
}


def set_shown_operation(self, value):
    # This is extremely hacky but emulates dynamically adding or removing operations
    if value == 1:
        self.shown_ops += 1
        if self.shown_ops >= len(self.operations):
            self.shown_ops = len(self.operations)
    if value == 2:
        self.shown_ops -= 1


class OperationSetting(PropertyGroup):
    type: EnumProperty(
        name="Operation",
        items=[(op.MAPPING, op.LABEL, op.DESCRIPTION) for op in OPERATION_MAPPING.values()],
    )
    vector_value: FloatVectorProperty(name="Value")


class OperationSettings(PropertyGroup, CacheMapping):
    CACHE_MAPPING = "operation_settings"

    MAX_OPS = 15
    operation_internal: EnumProperty(
        items=(
            ("NONE",) * 3,
            ("+",) * 3,
            ("-",) * 3,
        ),
        set=set_shown_operation,
    )
    shown_ops: IntProperty(default=1, min=1)

    active: BoolProperty(default=False)
    operations: CollectionProperty(type=OperationSetting)

    def init(self):
        for _ in range(self.MAX_OPS):
            self.operations.add()

    def draw(self, layout, context):
        box = layout.box()
        row = box.row(align=True)
        row.prop(self, "active", text="Custom Operation", toggle=True, icon="MODIFIER")
        if self.active:
            row.prop_enum(self, "operation_internal", value="+", icon="ADD", text="")
            row.prop_enum(self, "operation_internal", value="-", icon="REMOVE", text="")
            for i in range(self.shown_ops):
                operation_pg = self.operations[i]
                op_box = box.box()
                op_box.prop(operation_pg, "type")
                operation_cls = OPERATION_MAPPING.get(operation_pg.type)
                if (
                    operation_cls
                    and not isinstance(operation_cls, NONE_OPERATION)
                    and hasattr(operation_cls, "OPERATOR")
                    and not operation_cls.OPERATOR
                ):
                    try:
                        op_box.prop(operation_pg, operation_cls.ATTRIBUTE, text=operation_cls.ATTRIBUTE_NAME)
                    except AttributeError:
                        op_box.prop(operation_pg, operation_cls.ATTRIBUTE)

    def execute(self, assets):
        if not self.active:
            return
        for i in range(self.shown_ops):
            operation_pg = self.operations[i]
            if isinstance(operation_pg, NONE_OPERATION):
                continue
            operation_cls = OPERATION_MAPPING.get(operation_pg.type)
            if not operation_cls:
                return
            if operation_cls.OPERATOR:
                operation = f"bpy.ops.{operation_cls.OPERATION}({{'{operation_cls.ATTRIBUTE}': assets}}, {operation_cls.ADDITIONAL_ATTRIBUTES})"
                exec(operation)
            else:
                value = getattr(operation_pg, operation_cls.ATTRIBUTE)
                operation_cls.OPERATION(assets, value)

    def copy(self, source):
        copy_simple_property_group(source, self)
        self.operations.clear()
        for op in source.operations:
            new_op = self.operations.add()
            copy_simple_property_group(op, new_op)
