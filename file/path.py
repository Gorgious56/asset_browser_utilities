from pathlib import Path
import bpy


def get_supported_images(folder, recursive):
    for ext in bpy.path.extensions_image:  # All supported image extensions in Blender
        if recursive:
            yield from [fp for fp in folder.glob("**/*" + ext) if fp.is_file()]
        else:
            yield from [fp for fp in folder.glob("*" + ext) if fp.is_file()]


def is_this_current_file(filepath):
    return bpy.data.filepath == filepath


def open_file_if_different_from_current(filepath: str):
    if not is_this_current_file(filepath):
        bpy.ops.wm.open_mainfile(filepath=str(filepath))


def read_lines_sequentially(filepath):
    with open(filepath) as file:
        while True:
            try:
                yield next(file)
            except StopIteration:
                break


def get_folder_from_path(path):
    path = Path(path)
    if path.is_dir():
        return path
    else:
        return path.parent
