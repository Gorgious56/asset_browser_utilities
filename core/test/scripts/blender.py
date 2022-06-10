from asset_browser_utilities.core.console.parser import ArgumentsParser

import asset_browser_utilities.module.asset.test.mark as mark
import asset_browser_utilities.module.asset.test.unmark as unmark

import bpy
from inspect import getmembers, isfunction

_test_modules = (
    mark,
    unmark,
)


if __name__ == "__main__":
    parser = ArgumentsParser()
    source_filepath = parser.get_arg_value("source_filepath")
    tests = 0
    for module in _test_modules:
        for func_name, func in getmembers(module, isfunction):
            if str(func_name).startswith("test"):
                func(source_filepath)
                tests += 1
    print(f"~~~ All {tests} tests have sucessfully completed ~~~")
