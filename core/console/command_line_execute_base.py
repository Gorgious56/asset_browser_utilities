from asset_browser_utilities.core.console.parser import ArgumentsParser
import bpy

from asset_browser_utilities.core.library.prop import LibraryExportSettings
from asset_browser_utilities.core.cache.tool import get_current_operator_properties, get_from_cache
from asset_browser_utilities.core.file.save import save_file


class CommandLineExecuteBase:
    thread_index: int
    filepath: str

    def __init__(self) -> None:
        parser = ArgumentsParser()
        self.attributes = {
            attr_name: attr_type(parser.get_arg_value(attr_name))
            for attr_name, attr_type in self.__class__.__annotations__.items()
        }

    def run(self):
        op_props = get_current_operator_properties()
        should_save = op_props.run_in_file(self.attributes)
        if should_save is None or bool(should_save):
            if getattr(op_props, "generate_previews", False):
                while bpy.app.is_job_running("RENDER_PREVIEW"):
                    pass
            save_file(remove_backup=get_from_cache(LibraryExportSettings).remove_backup)
        quit()
