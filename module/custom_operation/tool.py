from .static import OPERATION_MAPPING


def get_available_operations():
    for operation in OPERATION_MAPPING.values():
        if (hasattr(operation, "poll") and operation.poll()) or not hasattr(operation, "poll"):
            yield operation


def update_operations_amount(self, value):
    # This is extremely hacky but emulates dynamically adding or removing operations
    self.ensure_operations_amount()
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
