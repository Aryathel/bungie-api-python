import re


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
    def indent_str(cls, content: str, depth: int):
        return f'{cls.indent * depth}{content}'

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
                rind = line.rindex(' ')
                while rind + prefix_length > cls.max_line_length:
                    rind = line.rindex(' ', 0, rind)
                lines.append(line[:rind])
                lines += cls.split_text_for_wrapping(line[rind+1:], prefix_length)
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