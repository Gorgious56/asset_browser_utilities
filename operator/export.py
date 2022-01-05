import os.path
import functools
import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty, PointerProperty

from asset_browser_utilities.prop.filter_type import FilterTypes
from asset_browser_utilities.prop.filter_name import FilterName


class ASSET_OT_export(Operator, ExportHelper):
    bl_idname = "asset.export"
    bl_label = "Export Assets"
    
    filter_glob: StringProperty(
        default="*.blend",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    
    filename_ext = ".blend"   
     
    filter_types: PointerProperty(type=FilterTypes)
    filter_name: PointerProperty(type=FilterName)
    filter_selection: BoolProperty()
    
    def invoke(self, context, event):
        self.filter_types.initialize()
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}
        return context.window_manager.invoke_props_dialog(self)
        
    def execute(self, context):
        filepath = self.filepath
        if bpy.data.filepath == filepath:
            return {'FINISHED'}   
        source_file = bpy.data.filepath
        if bpy.data.is_saved and bpy.data.is_dirty:
            bpy.ops.wm.save_mainfile()

        assets = []
        self.filter_types.populate(assets)
        self.filter_name.filter(assets)
        if self.filter_selection:
            assets = [a for a in assets if a.select_get()]

        asset_names = [a.name for a in assets]
        asset_types = [type(a).__name__ for a in assets]
            
        if os.path.isfile(filepath):
            bpy.ops.wm.open_mainfile(filepath=filepath)
        else:
            bpy.ops.wm.read_homefile(app_template="")
            bpy.ops.wm.save_as_mainfile(filepath=filepath)

        del assets  # Don't keep this in memory since it has been invalidated by loading a new file
        for name, _type in zip(asset_names, asset_types):
            bpy.app.timers.register(
                functools.partial(
                    append,
                    os.path.join(source_file, _type, name), 
                    os.path.join(source_file, _type), 
                    name),
                first_interval=0.1
            )  # Have to delay a bit else context is incorrect
        bpy.ops.wm.save_mainfile()

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "filter_selection", text="Only Selected", icon="RESTRICT_SELECT_OFF")
        self.filter_types.draw(layout)
        self.filter_name.draw(layout)
 
def append(filepath, directory, filename):          
    bpy.ops.wm.append(
        filepath=filepath,
        directory=directory,
        filename=filename
        )
