from asset_browser_utilities.core.log.logger import Logger
import bpy  # Do not remove even if it seems unused !!
from bpy.types import PropertyGroup
from bpy.props import (
    EnumProperty,
    BoolProperty,
    FloatVectorProperty,
    CollectionProperty,
    IntProperty,
    StringProperty,
)
from asset_browser_utilities.core.tool import copy_simple_property_group
from asset_browser_utilities.core.cache.tool import CacheMapping
from asset_browser_utilities.module.transform.operation import (
    ApplyTransformOperation,
    ApplyLocationOperation,
    ApplyScaleOperation,
    ApplyRotationOperation,
    TranslateOperation,
    ScaleOperation,
    RotateOperation,
)
from asset_browser_utilities.module.mesh.operation import DecimateOperation
from asset_browser_utilities.module.asset.operation import RenameAssetOperation, RenameDataOperation, RenameMaterialOperation


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
    DecimateOperation.MAPPING: DecimateOperation,
    RenameAssetOperation.MAPPING: RenameAssetOperation,
    RenameDataOperation.MAPPING: RenameDataOperation,
    RenameMaterialOperation.MAPPING: RenameMaterialOperation,
}


def set_shown_operation(self, value):
    # This is extremely hacky but emulates dynamically adding or removing operations
    if value == 1:
        self.shown_ops += 1
        if self.shown_ops >= len(self.operations):
            self.shown_ops = len(self.operations)
    if value == 2:
        self.shown_ops -= 1


def get_enum_items(self, context):
    operation_cls = OPERATION_MAPPING.get(self.type)
    if hasattr(operation_cls, "get_enum_items"):
        return operation_cls.get_enum_items()
    else:
        return [("NONE",) * 3]


class OperationSetting(PropertyGroup):
    type: EnumProperty(
        name="Operation",
        items=[(op.MAPPING, op.LABEL, op.DESCRIPTION) for op in OPERATION_MAPPING.values()],
    )
    vector_value: FloatVectorProperty(name="Value")
    int_value: IntProperty(name="Value")
    bool_value: BoolProperty(name="Value")
    enum_value: EnumProperty(items=get_enum_items)
    string_value: StringProperty(name="Value")
    string_value_2: StringProperty(name="Value")


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
                if operation_cls and not isinstance(operation_cls, NONE_OPERATION):
                    if hasattr(operation_cls, "draw"):
                        operation_cls.draw(op_box, operation_pg)
                        continue
                    elif hasattr(operation_cls, "ATTRIBUTE"):
                        attributes = [operation_cls.ATTRIBUTE]
                        attributes_names = (
                            [operation_cls.ATTRIBUTE_NAME] if hasattr(operation_cls, "ATTRIBUTE_NAME") else [None]
                        )
                    elif hasattr(operation_cls, "ATTRIBUTES"):
                        attributes = operation_cls.ATTRIBUTES
                        attributes_names = operation_cls.ATTRIBUTES_NAMES
                    else:
                        continue
                    for attr, name in zip(attributes, attributes_names):
                        if name is not None:
                            op_box.prop(operation_pg, attr, text=name)
                        else:
                            op_box.prop(operation_pg, attr)

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
            if hasattr(operation_cls, "ATTRIBUTE"):
                value = getattr(operation_pg, operation_cls.ATTRIBUTE)
                operation_cls.OPERATION(assets, value)
            elif hasattr(operation_cls, "ATTRIBUTES"):
                values = [getattr(operation_pg, attr) for attr in operation_cls.ATTRIBUTES]
                operation_cls.OPERATION(assets, *values)
            else:
                operation_cls.OPERATION(assets)
            Logger.display(f"Successfully applied '{operation_cls.LABEL}' to assets : {list(assets)}")

    def copy_from(self, source):
        copy_simple_property_group(source, self)
        self.operations.clear()
        for op in source.operations:
            new_op = self.operations.add()
            copy_simple_property_group(op, new_op)
