import re
from typing import Optional, Any


class StringUtils:
    max_line_length = 120
    indent = '    '

    @staticmethod
    def gen_import(pkg: str, imp: list[str] = None, relative: bool = False) -> str:
        if relative:
            pkg = f'.{pkg}'

        if imp:
            return f'from {pkg} import {", ".join(imp)}'
        else:
            return f'import {pkg}'

    @classmethod
    def wrap_import(cls, imp: str) -> str:
        if len(imp) < cls.max_line_length:
            return imp

        lines = cls.split_text_with_backslash(imp, 6)
        imp = lines[0] + ' \\\n'
        for i, l in enumerate(lines[1:]):
            imp += cls.indent_str(l, 1) + (' \\\n' if i < len(lines[1:])-1 else '')
        return imp

    @staticmethod
    def gen_class_declaration(class_name: str, inheritance: list[str] | str = None) -> str:
        if not inheritance:
            return f'class {class_name}:'
        else:
            if isinstance(inheritance, str):
                return f'class {class_name}({inheritance}):'
            else:
                return f'class {class_name}({", ".join(inheritance)}):'

    @classmethod
    def gen_function_declaration(
            cls,
            func_name: str,
            params: Optional[list[str]] = None,
            response_type: Optional[str] = None,
            is_async: bool = False,
            depth: int = 0,
    ) -> str:
        dec = f'{cls.indent * depth}{"async " if is_async else ""}def {func_name}({", ".join(params)})' \
               f'{" -> " + response_type if response_type else ""}:'
        if len(dec) > cls.max_line_length:
            dec = f'{cls.indent * depth}{"async " if is_async else ""}def {func_name}(\n'
            dec += '\n'.join(f'{cls.indent * (depth+2)}{p},' for p in params)
            dec += f'\n{cls.indent * depth}{") -> " + response_type if response_type else ")"}:'
        return dec

    @classmethod
    def indent_str(cls, content: str, depth: int):
        return '\n'.join(f'{cls.indent * depth}{c}' if c else "" for c in content.split('\n'))

    @staticmethod
    def camel_to_snake(inp: str) -> str:
        tmp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', inp)
        tmp2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', tmp).lower()
        return tmp2

    @classmethod
    def split_text_for_wrapping(cls, inp: str, prefix_length: int = 0) -> list[str]:
        lines = []
        inp = inp.split('\n')
        for line in inp:
            if len(line) + prefix_length > cls.max_line_length:
                try:
                    rind = line.rindex(' ')
                    while rind + prefix_length > cls.max_line_length:
                        try:
                            rind = line.rindex(' ', 0, rind)
                        except ValueError:
                            break
                    lines.append(line[:rind])
                    lines += cls.split_text_for_wrapping(line[rind + 1:], prefix_length)
                except ValueError:
                    lines.append(line)
            else:
                lines.append(line)
        return lines

    @classmethod
    def split_text_with_backslash(cls, inp: str, prefix_length: int = 0) -> list[str]:
        lines = []
        inp = inp.split('\n')
        prefix_length += 2
        for line in inp:
            if len(line) + prefix_length > cls.max_line_length:
                try:
                    rind = line.rindex(' ')
                    while rind + prefix_length > cls.max_line_length:
                        try:
                            rind = line.rindex(' ', 0, rind)
                        except ValueError:
                            break
                    lines.append(line[:rind])
                    lines += cls.split_text_for_wrapping(line[rind + 1:], prefix_length)
                except ValueError:
                    lines.append(line)
            else:
                lines.append(line)
        return lines

    @classmethod
    def gen_comment(cls, inp: str, depth: int = 0) -> str:
        comment = ''
        for line in cls.split_text_for_wrapping(inp, len(f'{cls.indent*depth}# ')):
            if comment:
                comment += '\n'
            comment += f'{cls.indent*depth}# {line}'
        return comment

    @classmethod
    def gen_docstring(cls, body: str, depth: int = 0) -> str:
        comment = f'{cls.indent * depth}"""'
        for line in cls.split_text_for_wrapping(body, len(cls.indent * depth)):
            if comment:
                comment += '\n'
            comment += f'{cls.indent * depth}{line}'
        comment += f'\n{cls.indent*depth}"""'
        return comment

    @classmethod
    def gen_line_break_comment(cls, inp: str, depth: int = 0) -> str:
        prefix = f'{cls.indent * depth}# --- '
        return f'{prefix}{inp + " ":-<{cls.max_line_length - len(prefix)}}'

    @classmethod
    def get_class_name_from_ref_str(cls, ref: str) -> str:
        return ref.split('/')[-1].split('.')[-1].replace('[]', 'Array')
