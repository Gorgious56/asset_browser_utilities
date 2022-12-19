import bpy.app.timers
from bpy.types import Operator, PropertyGroup
from bpy.props import PointerProperty, BoolProperty, EnumProperty, CollectionProperty, IntProperty

from asset_browser_utilities.core.cache.tool import get_current_operator_properties
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.tool import copy_simple_property_group
from asset_browser_utilities.core.operator.tool import BatchExecute, BatchFolderOperator

from asset_browser_utilities.module.custom_operation.prop import OperationSetting
from asset_browser_utilities.module.custom_operation.tool import set_shown_operation
from asset_browser_utilities.module.custom_operation.static import OPERATION_MAPPING, NONE_OPERATION


class OperationCustomBatchExecute(BatchExecute):
    def __init__(self):
        self.asset = None
        self.operation = -1
        super().__init__()
    
    def execute_one_file_and_the_next_when_finished(self):
        operator_properties = get_current_operator_properties()
        if not self.assets:
            self.execute_next_file()
            return
        operator_properties = get_current_operator_properties()
        
        if operator_properties.operate_in_batches:
            self.execute_in_batches(self.assets)
            self.save_file()
            self.execute_next_file()
        else:
            bpy.app.timers.register(self.execute_in_sequence)

    def execute_in_sequence(self):
        if self.asset is None:
            if not self.assets:
                self.save_file()
                self.execute_next_file()
                return
            self.asset = self.assets.pop(0)
        
        operator_properties = get_current_operator_properties()
        if self.operation < operator_properties.shown_ops - 1:
            self.operation += 1
            operation_pg = operator_properties.operations[self.operation]
            if isinstance(operation_pg, NONE_OPERATION):
                return 0.01
            operation_cls = OPERATION_MAPPING.get(operation_pg.type)
            if not operation_cls or operation_cls == NONE_OPERATION:
                return 0.01
            if hasattr(operation_cls, "ATTRIBUTE"):
                value = getattr(operation_pg, operation_cls.ATTRIBUTE)
                operation_cls.OPERATION([self.asset], value)
            elif hasattr(operation_cls, "ATTRIBUTES"):
                values = [getattr(operation_pg, attr) for attr in operation_cls.ATTRIBUTES]
                operation_cls.OPERATION([self.asset], *values)
            else:
                operation_cls.OPERATION([self.asset])
            Logger.display(f"Successfully Done '{operation_cls.LABEL}' to asset : {self.asset}")
            return 0.01
        else:
            self.asset = None
            self.operation = -1
            return 0.01
        
    
    def execute_in_batches(self, assets):
        operator_properties = get_current_operator_properties()
        for i in range(operator_properties.shown_ops):
            operation_pg = operator_properties.operations[i]
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
        


class OperationCustomOperatorProperties(PropertyGroup):
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
        self.active = True
        for _ in range(self.MAX_OPS):
            self.operations.add()

    def copy_from(self, source):
        copy_simple_property_group(source, self)
        self.operations.clear()
        for op in source.operations:
            new_op = self.operations.add()
            copy_simple_property_group(op, new_op)


class ABU_OT_operation_custom(Operator, BatchFolderOperator):
    bl_idname = "abu.operation_custom"
    bl_label = "Execute Custom Operations"
    bl_options = {"REGISTER", "UNDO"}

    operator_settings: PointerProperty(type=OperationCustomOperatorProperties)
    logic_class = OperationCustomBatchExecute

    def invoke(self, context, event):
        return self._invoke(context, filter_assets=True)
