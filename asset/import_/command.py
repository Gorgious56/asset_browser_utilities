from asset_browser_utilities.asset.import_.helper import BatchExecute
from asset_browser_utilities.console.parser import ArgumentsParser

if __name__ == "__main__":
    parser = ArgumentsParser()
    blends = parser.get_arg_values("blends")

    operator_logic = BatchExecute(blends)
    operator_logic.execute()
