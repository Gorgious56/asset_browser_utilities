import bpy.app.timers
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty, EnumProperty, CollectionProperty, IntProperty

from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.tool import copy_simple_property_group
from asset_browser_utilities.core.operator.tool import BatchFolderOperator, BaseOperatorProps

from asset_browser_utilities.module.custom_operation.prop import OperationSetting
from asset_browser_utilities.module.custom_operation.tool import set_shown_operation
from asset_browser_utilities.module.custom_operation.static import OPERATION_MAPPING, NONE_OPERATION


class OperationCustomOperatorProperties(PropertyGroup, BaseOperatorProps):
    MAX_OPS = 15

    operate_in_batches: BoolProperty(
        default=True,
        name="Operate in Batches",
        description="Check this to apply the first operation to all assets, then the second operation, etc. \
If unchecked, each operation is applied to the first asset, \
then each operation is applied to the second asset, etc.",
    )
    operation_internal: EnumProperty(
        items=(
            ("NONE",) * 3,
            ("+",) * 3,
            ("-",) * 3,
        ),
        set=set_shown_operation,
    )
    shown_ops: IntProperty(default=1, min=1)
    operations: CollectionProperty(type=OperationSetting)

    def draw(self, layout, context=None):
        box = layout.box()
        box.prop(self, "operate_in_batches")
        row = box.row(align=True)
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

    def init(self):
        self.asset = None
        self.operation = -1
        self.active = True
        for _ in range(self.MAX_OPS):
            self.operations.add()

    def copy_from(self, source):
        copy_simple_property_group(source, self)
        self.operations.clear()
        for op in source.operations:
            new_op = self.operations.add()
            copy_simple_property_group(op, new_op)

    def run_in_file(self, attributes=None):
        if self.operate_in_batches:
            self.execute_in_batches(self.get_assets())
        else:
            for asset in self.get_assets():
                self.run_on_asset(asset)

    def run_on_asset(self, asset):
        if self.operation < self.shown_ops - 1:
            self.operation += 1
            operation_pg = self.operations[self.operation]
            if isinstance(operation_pg, NONE_OPERATION):
                return 0.01
            operation_cls = OPERATION_MAPPING.get(operation_pg.type)
            if not operation_cls or operation_cls == NONE_OPERATION:
                return 0.01
            if hasattr(operation_cls, "ATTRIBUTE"):
                value = getattr(operation_pg, operation_cls.ATTRIBUTE)
                operation_cls.OPERATION([asset], value)
            elif hasattr(operation_cls, "ATTRIBUTES"):
                values = [getattr(operation_pg, attr) for attr in operation_cls.ATTRIBUTES]
                operation_cls.OPERATION([asset], *values)
            else:
                operation_cls.OPERATION([asset])
            Logger.display(f"Successfully Done '{operation_cls.LABEL}' to asset : {asset}")

    def execute_in_batches(self, assets):
        for i in range(self.shown_ops):
            operation_pg = self.operations[i]
            if isinstance(operation_pg, NONE_OPERATION):
                continue
            operation_cls = OPERATION_MAPPING.get(operation_pg.type)
            if not operation_cls or operation_cls == NONE_OPERATION:
                continue
            if hasattr(operation_cls, "ATTRIBUTE"):
                value = getattr(operation_pg, operation_cls.ATTRIBUTE)
                operation_cls.OPERATION(assets, value)
            elif hasattr(operation_cls, "ATTRIBUTES"):
                values = [getattr(operation_pg, attr) for attr in operation_cls.ATTRIBUTES]
                operation_cls.OPERATION(assets, *values)
            else:
                operation_cls.OPERATION(assets)
            Logger.display(f"Successfully Done '{operation_cls.LABEL}' to assets : {list(assets)}")


class ABU_OT_operation_custom(Operator, BatchFolderOperator):
    bl_idname = "abu.operation_custom"
    bl_label = "Execute Custom Operations"
    bl_options = {"REGISTER", "UNDO"}

    operator_settings: PointerProperty(type=OperationCustomOperatorProperties)

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
