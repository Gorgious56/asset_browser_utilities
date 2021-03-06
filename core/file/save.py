from asset_browser_utilities.core.log.logger import Logger
import bpy
import os


def save_if_possible_and_necessary():
    if bpy.data.is_saved and bpy.data.is_dirty:
        save_file()


def create_new_file_and_set_as_current(filepath):
    bpy.ops.wm.read_homefile(app_template="")
    save_file_as(str(filepath))


def get_backup_path(filepath):
    return filepath + "1"


def has_backup(filepath):
    backup = get_backup_path(filepath)
    return os.path.exists(backup)


def remove_backup_file_if_it_exists(filepath):
    if has_backup(filepath):
        backup = get_backup_path(filepath)
        Logger.display("Removing backup " + backup)
        os.remove(backup)


def save_file(remove_backup=False):
    try:
        bpy.ops.wm.save_mainfile()
    except RuntimeError as e:
        print(e)
        print(f"Skipping file {bpy.data.filepath}. Please make sure linked libraries are valid in this file.")
    else:        
        if remove_backup and has_backup(bpy.data.filepath):
            remove_backup_file_if_it_exists(bpy.data.filepath)


def save_file_as(filepath: str, remove_backup=False):
    if not filepath:
        return
    had_backup = has_backup(filepath)
    bpy.ops.wm.save_as_mainfile(filepath=str(filepath))
    if remove_backup and not had_backup:
        remove_backup_file_if_it_exists(filepath)
