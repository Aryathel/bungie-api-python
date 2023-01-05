import os

from ..utils.str_utils import StringUtils


class EntityTree:
    folders = dict[str, dict]

    def __init__(self) -> None:
        self.folders = {}

    def __getitem__(self, item):
        return self.folders[item]

    def add_item(self, qualified_name: str) -> None:
        qualified_name = qualified_name.replace('[]', 'Array')

        cur = self.folders
        name = qualified_name.split('.')
        for i, segment in enumerate(name):
            if not i >= len(name)-1:
                path = StringUtils.camel_to_snake(segment)
                if path not in cur:
                    cur[path] = {}
                cur = cur[path]
            else:
                cur[StringUtils.camel_to_snake(segment)] = segment

    def definition_count(self, folder: dict = None) -> int:
        if not folder:
            folder = self.folders
        count = 0
        for k, v in folder.items():
            if isinstance(v, dict):
                count += self.definition_count(v)
            elif isinstance(v, str):
                count += 1
        return count

    def populate_init_files(self, root: str, folder: dict = None) -> None:
        if not folder:
            folder = self.folders

        imports = []
        _all = []

        for k, v in folder.items():
            if isinstance(v, str):
                imports.append(StringUtils.gen_import(k, imp=[v], relative=True))
                _all.append(v)
            elif isinstance(v, dict):
                self.populate_init_files(os.path.join(root, k), v)

        with open(os.path.join(root, '__init__.py'), 'w+') as init_file:
            content = '\n'.join(imports)
            content += '\n\n\n'
            content += '__all__ = [\n'
            content += '\n'.join([StringUtils.indent_str(f'\'{s}\',', 1) for s in sorted(_all)])
            content += '\n]\n'

            init_file.write(content)


