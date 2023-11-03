from pathlib import Path

from asset_browser_utilities.core.console.parser import ArgumentsParser
from asset_browser_utilities.core.log.logger import Logger
from asset_browser_utilities.core.file.path import open_file_if_different_from_current
from asset_browser_utilities.core.file.save import create_new_file_and_set_as_current, save_file, sanitize_filepath
from asset_browser_utilities.core.library.tool import append_asset


if __name__ == "__main__":
    parser = ArgumentsParser()
    asset_names = parser.get_arg_values(arg_name="asset_names", next_arg_name="asset_types")
    asset_types = parser.get_arg_values(arg_name="asset_types", next_arg_name="source_file")
    source_file = parser.get_arg_value("source_file")
    filepath = parser.get_arg_value("filepath")
    folder = parser.get_arg_value("folder")
    remove_backup = parser.get_arg_value("remove_backup", bool)
    overwrite = parser.get_arg_value("overwrite", bool)
    individual_files = parser.get_arg_value("individual_files", bool)
    type_folders = parser.get_arg_value("type_folders", bool)

    if individual_files:
        for asset_name, asset_type in zip(asset_names, asset_types):
            filepath = Path(folder)
            if type_folders:
                filepath /= asset_type
            filepath /= asset_name + ".blend"
            if filepath.exists():
                open_file_if_different_from_current(str(filepath))
            else:
                create_new_file_and_set_as_current(str(filepath))
            append_asset(source_file, asset_type, asset_name)
            save_file(remove_backup=remove_backup)
            Logger.display(f"Exported Asset '{asset_type}/{asset_name}' to '{sanitize_filepath(filepath)}'")
    else:
        if Path(filepath).exists():
            open_file_if_different_from_current(filepath)
        else:
            create_new_file_and_set_as_current(filepath)
        for asset_name, asset_type in zip(asset_names, asset_types):
            append_asset(source_file, asset_type, asset_name)
            Logger.display(f"Exported Asset '{asset_type}/{asset_name}' to '{filepath}'")
        save_file(remove_backup=remove_backup)

    quit()
