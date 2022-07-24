import sys

from inspect import getmembers, isfunction

from asset_browser_utilities.core.console.parser import ArgumentsParser


if __name__ == "__main__":
    parser = ArgumentsParser()
    source_filepath = parser.get_arg_value("source_filepath")
    tests = 0
    # https://stackoverflow.com/a/4858123/7092409
    for module_name, module in sys.modules.items():
        if not module_name.startswith("asset_browser_utilities.module") or "test" not in module_name:
            continue
        for func_name, func in getmembers(module, isfunction):
            if str(func_name).startswith("test"):
                print(f"   ~~~ {func.__name__} from {module.__name__} ~~~")
                func(source_filepath)
                tests += 1
    print(f"\n   ~~~ All {tests} tests have sucessfully completed ~~~")
