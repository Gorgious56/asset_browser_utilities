import bpy

from asset_browser_utilities.core.library.tool import link_asset, append_asset, get_blend_data_name_from_directory
from asset_browser_utilities.core.log.logger import Logger

from asset_browser_utilities.module.library.tool import ensure_asset_uuid


def replace_asset_with_linked_one(asset_to_discard, filepath, directory, name, create_liboverrides=False):
    linked_asset = link_asset(filepath, directory, name, create_liboverrides=create_liboverrides)
    Logger.display(f"Linked Asset '{repr(linked_asset)}' from {filepath}'")
    asset_to_discard.asset_clear()
    asset_to_discard.use_fake_user = False
    asset_to_discard.user_remap(linked_asset)
    Logger.display(f"Remapped users of old asset `{repr(asset_to_discard)}' to {linked_asset.library.filepath}/{repr(linked_asset)}'")

    for library in bpy.data.libraries:
        if library.filepath == filepath:
            new_dummy = library.abu_asset_library_dummy.assets.add()
            new_dummy.filepath = filepath
            new_dummy.directory = directory
            new_dummy.name = name
            new_dummy.uuid = ensure_asset_uuid(linked_asset)
            new_dummy.asset.set(linked_asset)
            break


def replace_with_asset_dummy(asset_dummy, asset_to_discard, purge=False):
    append_asset(asset_dummy.filepath, asset_dummy.directory, asset_dummy.name, overwrite=True)
    try:
        asset_to_discard.name
    except ReferenceError:
        pass
    else:
        bpy.data.batch_remove([asset_to_discard])
    if purge:
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)


def link_from_asset_dummy(asset_dummy, asset_to_discard, purge=False):
    filepath, directory, name = (
        asset_dummy.filepath,
        asset_dummy.directory,
        asset_dummy.name,
    )
    replace_asset_with_linked_one(asset_to_discard, filepath, directory, name, create_liboverrides=False)

    if purge:
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
