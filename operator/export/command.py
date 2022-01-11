from asset_browser_utilities.operator.export.logic import OperatorLogic

if __name__ == "__main__":
    import sys
    import json

    argv = sys.argv
    argv = argv[argv.index("--") + 1 :]  # get all args after "--"

    asset_names = []
    asset_names_start = argv.index("--asset_names")
    asset_types = []
    asset_types_start = argv.index("--asset_types")
    source_file_index = argv.index("--source_file")

    source_file = argv[source_file_index + 1]
    filepath = argv[argv.index("--filepath") + 1]
    prevent_backup = bool(json.loads(argv[argv.index("--prevent_backup") + 1]))
    overwrite = bool(json.loads(argv[argv.index("--overwrite") + 1]))
    individual_files = bool(json.loads(argv[argv.index("--individual_files") + 1]))

    for i in range(asset_names_start + 1, asset_types_start):
        asset_names.append(argv[i])
    for i in range(asset_types_start + 1, source_file_index):
        asset_types.append(argv[i])

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
