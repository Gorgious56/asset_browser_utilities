from asset_browser_utilities.core.console.parser import ArgumentsParser

import asset_browser_utilities.module.asset.test.mark
import asset_browser_utilities.module.asset.test.unmark
import asset_browser_utilities.module.asset.test.copy
import asset_browser_utilities.module.author.test.set
import asset_browser_utilities.module.description.test.set
import asset_browser_utilities.module.catalog.test.move_from_a_to_b
import asset_browser_utilities.module.catalog.test.move_to
import asset_browser_utilities.module.catalog.test.remove_from
import asset_browser_utilities.module.catalog.test.remove_empty
import asset_browser_utilities.module.preview.test.extract
import asset_browser_utilities.module.preview.test.import_

from inspect import getmembers, isfunction

_test_modules = (
    asset_browser_utilities.module.asset.test.mark,
    asset_browser_utilities.module.asset.test.unmark,
    asset_browser_utilities.module.asset.test.copy,
    asset_browser_utilities.module.author.test.set,
    asset_browser_utilities.module.description.test.set,
    asset_browser_utilities.module.catalog.test.move_from_a_to_b,
    asset_browser_utilities.module.catalog.test.move_to,
    asset_browser_utilities.module.catalog.test.remove_from,
    asset_browser_utilities.module.catalog.test.remove_empty,
    asset_browser_utilities.module.preview.test.extract, 
    asset_browser_utilities.module.preview.test.import_,
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
