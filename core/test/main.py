import json
import subprocess
from pathlib import Path
import os
import sys
import importlib.util

def test_blender():
    test_folder = Path(__file__).parent
    script = test_folder.parent / "console" / "builder.py"
    console = import_module_by_path(script)
    command = console.CommandBuilder(Path(os.path.realpath(__file__)).parent / "scripts/blender.py", "blender")
    command.add_arg_value("source_filepath", str(test_folder / "files" / "source.blend"))
    command.call()
    
    
def import_module_by_path(path):
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

if __name__ == "__main__":
    test_blender()
