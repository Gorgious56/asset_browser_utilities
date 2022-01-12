import os
from pathlib import Path
import bpy


def get_blend_files(settings):
    if settings.library_settings.this_file_only:
        return [str(bpy.data.filepath)]
    else:
        folder = Path(settings.filepath)
        if not folder.is_dir():
            folder = folder.parent
        if settings.library_settings.recursive:
            return [fp for fp in folder.glob("**/*.blend") if fp.is_file()]
        else:
            return [fp for fp in folder.glob("*.blend") if fp.is_file()]


def get_supported_images(folder, recursive):
    for ext in bpy.path.extensions_image:  # All supported image extensions in Blender
        if recursive:
            yield [fp for fp in folder.glob("**/*" + ext) if fp.is_file()]
        else:
            yield [fp for fp in folder.glob("*" + ext) if fp.is_file()]


def is_this_current_file(filepath):
    return bpy.data.filepath == filepath


def save_if_possible_and_necessary():
    if bpy.data.is_saved and bpy.data.is_dirty:
        bpy.ops.wm.save_mainfile()


def create_new_file_and_set_as_current(filepath):
    bpy.ops.wm.read_homefile(app_template="")
    save_file_as(filepath)


def remove_backup_file(filepath):
    backup = filepath + "1"
    if os.path.exists(backup):
        print("Removing backup " + backup)
        os.remove(backup)


def save_file(remove_backup=False):
    save_if_possible_and_necessary()
    if remove_backup:
        remove_backup_file(bpy.data.filepath)


def save_file_as(filepath: str, remove_backup=False):
    bpy.ops.wm.save_as_mainfile(filepath=filepath)
    if remove_backup:
        remove_backup_file(filepath)


def open_file_if_different_from_current(filepath: str):
    if not is_this_current_file(filepath):
        bpy.ops.wm.open_mainfile(filepath=filepath)


def get_catalog_file(filepath):
    folder = Path(filepath).parent
    return os.path.join(folder, "blender_assets.cats.txt")


def has_catalogs(filepath):
    return os.path.exists(get_catalog_file(filepath))


def read_lines_sequentially(filepath):
    with open(filepath) as file:
        while True:
            try:
                yield next(file)
            except StopIteration:
                break
