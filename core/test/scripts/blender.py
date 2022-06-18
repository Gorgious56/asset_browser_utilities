from asset_browser_utilities.core.console.parser import ArgumentsParser

from asset_browser_utilities.module.asset.test import mark, unmark, copy
from asset_browser_utilities.module.author.test import set as set_author
from asset_browser_utilities.module.description.test import set as set_description
from asset_browser_utilities.module.catalog.test import move_from_a_to_b, move_to, remove_from

from inspect import getmembers, isfunction

_test_modules = (
    mark,
    unmark,
    copy,
    set_author,
    set_description,
    move_from_a_to_b,
    move_to,
    remove_from,
)


if __name__ == "__main__":
    parser = ArgumentsParser()
    source_filepath = parser.get_arg_value("source_filepath")
    tests = 0
    for module in _test_modules:
        for func_name, func in getmembers(module, isfunction):
            if str(func_name).startswith("test"):
                print(f"   ~~~ {func.__name__} from {module.__name__} ~~~")
                func(source_filepath)
                tests += 1
    print(f"\n   ~~~ All {tests} tests have sucessfully completed ~~~")
