from pathlib import Path
import bpy


def get_blend_files(settings):
    if settings.library_export_settings.this_file_only:
        return [str(bpy.data.filepath)]
    else:
        folder = Path(settings.filepath)
        if not folder.is_dir():
            folder = folder.parent
        if settings.library_export_settings.recursive:
            return [fp for fp in folder.glob("**/*.blend") if fp.is_file()]
        else:
            return [fp for fp in folder.glob("*.blend") if fp.is_file()]

def is_this_current_file(filepath):
    return bpy.data.filepath == filepath

def save_if_possible_and_necessary():
    if bpy.data.is_saved and bpy.data.is_dirty:
        bpy.ops.wm.save_mainfile()

def create_new_file_and_set_as_current(filepath):    
    bpy.ops.wm.read_homefile(app_template="")
    bpy.ops.wm.save_as_mainfile(filepath=filepath)