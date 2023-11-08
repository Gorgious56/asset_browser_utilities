from pathlib import Path
import typing
import bpy
from asset_browser_utilities.core.cache.tool import get_from_cache
from asset_browser_utilities.module.asset.prop import SelectedAssetFiles


def ensure_object_is_not_asset(obj):
    obj.asset_clear()


def is_asset(obj):
    return obj.asset_data is not None


def all_assets():
    for d in dir(bpy.data):
        container = getattr(bpy.data, d)
        if "bpy_prop_collection" in str(type(container)):
            for asset in container:
                if is_asset(asset):
                    yield asset.asset_data


def all_assets_container_and_name():
    asset_names = []
    for d in dir(bpy.data):
        container = getattr(bpy.data, d)
        if "bpy_prop_collection" in str(type(container)):
            for asset in container:
                if is_asset(asset):
                    asset_names.append((d, asset.name))
    return asset_names


def get_selected_asset_files_cache():
    return get_from_cache(SelectedAssetFiles)


def get_selected_assets_fullpaths(context=None) -> typing.Iterable[Path]:
    # https://blender.stackexchange.com/a/261321/86891
    if context is None:
        context = bpy.context
    current_library_name = context.area.spaces.active.params.asset_library_ref

    if current_library_name == "LOCAL":  # Current file
        library_path = Path(bpy.data.filepath)
        for asset_file in context.selected_asset_files:
            yield library_path / asset_file.relative_path / asset_file.local_id.name
    else:
        library_path = Path(context.preferences.filepaths.asset_libraries.get(current_library_name).path)
        for asset_file in context.selected_asset_files:
            yield library_path / asset_file.relative_path


def get_selected_assets_folderpaths(context=None) -> typing.Iterable[Path]:
    if context is None:
        context = bpy.context
    return set(p.parents[2] for p in get_selected_assets_fullpaths(context))


def get_selected_linked_objects_in_outliner(context=None):
    context = context or bpy.context
    selected_assets = set(context.selected_ids)
    selected_assets.update(context.selected_objects)
    for selected_id in context.selected_ids:
        if hasattr(selected_id, "type") and selected_id.type == "EMPTY" and selected_id.instance_type:
            selected_id = selected_id.instance_collection
        if selected_id.library:
            yield selected_id.library.filepath
