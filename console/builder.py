import subprocess
import json
from collections import defaultdict


class CommandBuilder:
    def __init__(self, script_filepath) -> None:
        directory = script_filepath.parent
        self.command_path = directory / "command.py"
        self.expression = ""
        self.args = defaultdict(list)

    def build_expression(self):
        self.expression = "blender --python " + json.dumps(str(self.command_path)) + " --"
        # defaultdic is ordered so we can do this reliably https://stackoverflow.com/a/52174324/7092409
        for arg in self.args.keys():
            self.expression += " --" + arg
            for value in self.args[arg]:
                self.expression += " " + json.dumps(value)

    def add_arg_value(self, arg_name, value):
        self.args[arg_name].append(value)

    def call(self):
        self.build_expression()
        subprocess.call(self.expression)
