from pathlib import Path


def get_exported_asset_filepath(root_folder, asset_folder, asset_name, catalog_folders: bool):
    filepath = Path(root_folder)
    if catalog_folders and asset_folder:
        for subfolder in asset_folder.split("/"):
            filepath /= subfolder
    filepath /= asset_name + ".blend"
    return filepath
