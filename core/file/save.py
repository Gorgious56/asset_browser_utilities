from pathlib import Path
import os
import bpy
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.preferences.tool import get_preferences


def save_if_possible_and_necessary():
    if bpy.data.is_saved and bpy.data.is_dirty:
        save_file()


def is_ascii_alnum(character):
    return "A" <= character <= "Z" or "a" <= character <= "z" or "0" <= character <= "9"


def sanitize_filepath(filepath, replace_with="_"):
    filepath_pathlib = Path(filepath)
    stem = filepath_pathlib.stem
    new_stem = ""
    for char in stem:
        new_stem += char if is_ascii_alnum(char) else "_"
    filepath_pathlib = filepath_pathlib.with_stem(new_stem.strip())
    return str(filepath_pathlib)


def create_new_file_and_set_as_current(filepath):
    filepath = sanitize_filepath(str(filepath))
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
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


def save_file(remove_backup=False, filepath=None):
    if filepath is None:
        filepath = bpy.data.filepath
    try:
        bpy.ops.wm.save_mainfile(compress=get_preferences().save_compress)
    except RuntimeError as e:
        print(e)
        print(f"Skipping file {filepath}. Please make sure linked libraries are valid in this file.")
    else:
        if remove_backup and has_backup(filepath):
            remove_backup_file_if_it_exists(filepath)


def save_file_as(filepath: str, remove_backup=False):
    if not filepath:
        return
    had_backup = has_backup(filepath)
    bpy.ops.wm.save_as_mainfile(filepath=str(filepath), compress=get_preferences().save_compress)
    if remove_backup and not had_backup:
        remove_backup_file_if_it_exists(filepath)
