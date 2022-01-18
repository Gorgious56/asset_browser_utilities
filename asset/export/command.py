from asset_browser_utilities.asset.export.helper import BatchExecute
from asset_browser_utilities.console.parser import ArgumentsParser

if __name__ == "__main__":
    parser = ArgumentsParser()
    asset_names = parser.get_arg_values("asset_names", "asset_types")
    asset_types = parser.get_arg_values("asset_types", "source_file")
    source_file = parser.get_arg_value("source_file")
    filepath = parser.get_arg_value("filepath")
    remove_backup = parser.get_arg_value("remove_backup", bool)
    overwrite = parser.get_arg_value("overwrite", bool)
    individual_files = parser.get_arg_value("individual_files", bool)

    operator_logic = BatchExecute(
        asset_names,
        asset_types,
        source_file,
        filepath,
        remove_backup,
        overwrite,
        individual_files,
    )
    operator_logic.execute()
