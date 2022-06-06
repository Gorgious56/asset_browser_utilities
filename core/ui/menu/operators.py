from asset_browser_utilities.library.prop import LibraryType


class ABUOperatorsMenu:
    ops = []

    def draw(self, context):
        self.ops.clear()
        self.setup_ops(self.layout, context)
        self.setup_library_source(LibraryType.get_library_type_from_context(context))
    
    def setup_ops(self, layout, context):
        pass

    def add_op(self, layout, command, text="", icon=None):
        if icon is not None:
            self.ops.append(layout.operator(command, text=text, icon=icon))
        else:
            self.ops.append(layout.operator(command, text=text))
    
    def setup_library_source(self, library_source):
        for op in self.ops:
            op.source = library_source
