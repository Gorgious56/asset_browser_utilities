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
from asset_browser_utilities.core.log.logger import Logger
from .tool import get_available_operations, get_enum_items, set_shown_operation
from .static import OPERATION_MAPPING, NONE_OPERATION


class OperationSetting(PropertyGroup):
    type: EnumProperty(
        name="Operation",
        items=lambda self, context: [(op.MAPPING, op.LABEL, op.DESCRIPTION) for op in get_available_operations()],
    )
    vector_value: FloatVectorProperty(name="Value")
    int_value: IntProperty(name="Value")
    bool_value: BoolProperty(name="Value")
    enum_value: EnumProperty(items=get_enum_items)
    string_value: StringProperty(name="Value")
    string_value_2: StringProperty(name="Value")


class OperationSettings(PropertyGroup):
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
