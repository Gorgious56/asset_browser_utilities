import bpy

from asset_browser_utilities.core.library.tool import link_asset
from asset_browser_utilities.core.log.logger import Logger


def replace_asset_with_linked_one(asset_to_discard, filepath, directory, name, create_liboverrides=False):
    linked_asset = link_asset(filepath, directory, name, create_liboverrides=create_liboverrides)
    Logger.display(f"Linked Asset '{directory}/{name}' from {filepath}'")
    asset_to_discard.user_remap(linked_asset)
    asset_to_discard.asset_clear()
    asset_to_discard.use_fake_user = False
    Logger.display(f"Remapped users of old asset `{repr(asset_to_discard)}' to {repr(linked_asset)}'")


def link_from_asset_dummy(asset_dummy, asset_to_discard, purge=False):
    filepath, directory, name = (
        asset_dummy.filepath,
        asset_dummy.directory,
        asset_dummy.name,
    )
    replace_asset_with_linked_one(asset_to_discard, filepath, directory, name, create_liboverrides=True)
    if purge:
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
