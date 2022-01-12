from asset_browser_utilities.operator.export.logic import OperatorLogic
from asset_browser_utilities.helper.command import ArgumentsParser

if __name__ == "__main__":
    import sys

    argv = sys.argv
    argv = argv[argv.index("--") + 1 :]  # get all args after "--"
    parser = ArgumentsParser(argv)
    asset_names = parser.get_arg_values("asset_names", "asset_types")
    asset_types = parser.get_arg_values("asset_types", "source_file")
    source_file = parser.get_arg_value("source_file")
    filepath = parser.get_arg_value("filepath")
    prevent_backup = parser.get_arg_value("prevent_backup", bool)
    overwrite = parser.get_arg_value("overwrite", bool)
    individual_files = parser.get_arg_value("individual_files", bool)

    operator_logic = OperatorLogic(
        asset_names,
        asset_types,
        source_file,
        filepath,
        prevent_backup,
        overwrite,
        individual_files,
    )
    operator_logic.execute()
