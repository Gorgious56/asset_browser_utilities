from asset_browser_utilities.core.console.parser import ArgumentsParser
import importlib.util
from pathlib import Path


if __name__ == "__main__":
    source_operator_file = ArgumentsParser().get_arg_value("source_operator_file")
    module_name = Path(source_operator_file).stem
    spec = importlib.util.spec_from_file_location(module_name, source_operator_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.CommandLineExecute().run()
