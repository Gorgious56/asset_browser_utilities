import bpy.types  # Do not remove even if it seems unused
from asset_browser_utilities.core.library.prop import LibraryType


class ABUOperatorsMenu:
    ops_cmd = []
    ops = []

    def draw(self, context):
        self.ops.clear()
        self.setup_ops(self.layout, context)
        self.setup_library_source(LibraryType.get_library_type_from_context(context))

    def setup_ops(self, layout, context):
        for op in self.ops_cmd:
            self.add_op(layout, context, *op)

    def add_op(self, layout, context, command, text="", icon=None, *op):
        library_source = LibraryType.get_library_type_from_context(context)
        ui_library = eval("bpy.types.ABU_OT_" + command.split(".")[1]).ui_library
        if ui_library == LibraryType.All or library_source == ui_library or library_source in ui_library:
            if icon is not None:
                self.ops.append(layout.operator(command, text=text, icon=icon))
            else:
                self.ops.append(layout.operator(command, text=text))
            for kv in op:
                for k, v in kv.items():
                    setattr(self.ops[-1], k, v)

    def setup_library_source(self, library_source):
        for op in self.ops:
            op.source = library_source
