import bpy

from asset_browser_utilities.core.console.parser import ArgumentsParser

import asset_browser_utilities.asset.test.mark

from inspect import getmembers, isfunction


def purge():
    bpy.data.batch_remove(bpy.data.objects)
    bpy.data.batch_remove(bpy.data.meshes)


_test_modules = (asset_browser_utilities.asset.test.mark,)


if __name__ == "__main__":
    parser = ArgumentsParser()
    source_filepath = parser.get_arg_value("source_filepath")
    for module in _test_modules:
        for func_name, func in getmembers(module, isfunction):
            if str(func_name).startswith("test"):
                func(source_filepath)
