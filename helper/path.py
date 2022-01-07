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
