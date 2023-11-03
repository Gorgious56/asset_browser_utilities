import bpy

from asset_browser_utilities.core.library.tool import link_asset

from asset_browser_utilities.core.log.logger import Logger


def link_from_asset_dummy(asset_dummy, asset_to_discard):
    filepath, directory, name = (
        asset_dummy.filepath,
        asset_dummy.directory,
        asset_dummy.name,
    )
    linked_asset = link_asset(filepath, directory, name)
    Logger.display(f"Linked Asset '{directory}/{name}' from {filepath}'")
    asset_to_discard.user_remap(linked_asset)
    asset_to_discard.asset_clear()
    asset_to_discard.use_fake_user = False
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    Logger.display(f"Remapped users of old asset `{repr(asset_to_discard)}' to {repr(linked_asset)}'")
