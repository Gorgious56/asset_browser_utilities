import json


class ArgumentsParser:
    def __init__(self, argv):
        self.argv = argv

    def get_arg_index(self, arg_name):
        return self.argv.index("--" + arg_name) + 1

    def get_arg_value(self, arg_name, cast=None):
        index = self.get_arg_index(arg_name)
        if cast is None:
            return self.argv[index]
        else:
            return cast(json.loads(self.argv[index]))

    def get_arg_values(self, arg_name, next_arg_name=None, cast=None):
        start = self.get_arg_index(arg_name)
        stop = (self.get_arg_index(next_arg_name) - 1) if next_arg_name is not None else len(self.argv)
        values = []
        for i in range(start, stop):
            if cast is None:
                values.append(self.argv[i])
            else:
                values.append(cast(self.argv[i]))
        return values
