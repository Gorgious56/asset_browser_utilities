import subprocess
import json
from collections import defaultdict


class CommandBuilder:
    def __init__(self, script_filepath, blend_filepath=None) -> None:
        self.command_path = script_filepath
        self.blend_filepath = blend_filepath or ""
        self.expression = ""
        self.args = defaultdict(list)

    def build_expression(self):
        if self.blend_filepath:
            self.expression = (
                f'blender "{str(self.blend_filepath)}" --background --python {json.dumps(str(self.command_path))} --'
            )
        else:
            self.expression = f"blender --background --python {json.dumps(str(self.command_path))} --"
        # defaultdict is ordered so we can do this reliably https://stackoverflow.com/a/52174324/7092409
        for arg in self.args.keys():
            self.expression += " --" + arg
            for value in self.args[arg]:
                self.expression += " " + json.dumps(value)

    def add_arg_value(self, arg_name, value):
        self.args[arg_name].append(value)

    def call(self):
        self.build_expression()
        subprocess.call(self.expression)
