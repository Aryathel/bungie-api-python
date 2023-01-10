import os

from .endpoints import EndpointCollection
from .entity_import import EntityImportCollection, EntityImport
from .enums import ImportType
from ..utils.str_utils import StringUtils


class Client:
    endpoints_path_name = 'endpoints'
    sync_client_name = 'BungieClientSync'
    async_client_name = 'BungieClientAsync'
    sync_client_file_name = 'client_sync'
    async_client_file_name = 'client_async'
    file_extension = '.py'

    def __init__(self, is_async: bool, endpoints: list[EndpointCollection]):
        self.is_async = is_async
        self.endpoints = endpoints

        self.imports = EntityImportCollection([
            EntityImport(
                name='typing',
                type=ImportType.stdlib,
                imports=['Optional', 'Any', 'Generator']
            )
        ])

        if self.is_async:
            self.imports.add_import(EntityImport(
                name='contextlib',
                type=ImportType.stdlib,
                imports=['asynccontextmanager']
            ))
            self.imports.add_import(EntityImport(
                name='aiohttp',
                type=ImportType.external,
            ))
            self.imports.add_import(EntityImport(
                name='aiohttp',
                type=ImportType.external,
                imports=['BasicAuth', 'ClientSession']
            ))
        else:
            self.imports.add_import(EntityImport(
                name='contextlib',
                type=ImportType.stdlib,
                imports=['contextmanager']
            ))
            self.imports.add_import(EntityImport(
                name='requests',
                type=ImportType.external,
            ))
            self.imports.add_import(EntityImport(
                name='requests.auth',
                type=ImportType.external,
                imports=['HTTPBasicAuth']
            ))
            self.imports.add_import(EntityImport(
                name='requests',
                type=ImportType.external,
                imports=['Session']
            ))

        self.imports.add_collection(EntityImportCollection([
            EntityImport(
                name=self.endpoints_path_name,
                type=ImportType.relative,
                imports=[n.name_async] if self.is_async else [n.name_sync]
            )
            for n in self.endpoints
        ]))

    @property
    def init_string(self) -> str:
        return EntityImport(
            name=self.file_name,
            type=ImportType.relative,
            imports=[self.name]
        ).import_string

    @property
    def get_method(self) -> list[str]:
        items = []
        if self.is_async:
            items.append('async def _get(')
            items.append(StringUtils.indent_str('self,', 2))
            items.append(StringUtils.indent_str('url: str,', 2))
            items.append(StringUtils.indent_str('params: Optional[dict[str, Any]] = None,', 2))
            items.append(StringUtils.indent_str('headers: Optional[dict[str, Any]] = None,', 2))
            items.append(StringUtils.indent_str('data: Optional[Any] = None,', 2))
            items.append(StringUtils.indent_str('json: Optional[dict[str, Any] | list[Any]] = None,', 2))
            items.append(StringUtils.indent_str('requires_oauth: bool = False,', 2))
            items.append(StringUtils.indent_str('auth: BasicAuth = None,', 2))
            items.append(') -> str:')
            items.append(StringUtils.indent_str(
                'async with self.session(with_oauth=requires_oauth) as session:',
                1
            ))
            items.append(StringUtils.indent_str('async with session.get(', 2))
            items.append(StringUtils.indent_str('url,', 3))
            items.append(StringUtils.indent_str('headers=headers,', 3))
            items.append(StringUtils.indent_str('params=params,', 3))
            items.append(StringUtils.indent_str('auth=auth,', 3))
            items.append(StringUtils.indent_str('data=data,', 3))
            items.append(StringUtils.indent_str('json=json,', 3))
            items.append(StringUtils.indent_str(') as r:', 2))
            items.append(StringUtils.indent_str('return await r.text()', 3))
        else:
            items.append('def _get(')
            items.append(StringUtils.indent_str('self,', 2))
            items.append(StringUtils.indent_str('url: str,', 2))
            items.append(StringUtils.indent_str('params: Optional[dict[str, Any]] = None,', 2))
            items.append(StringUtils.indent_str('headers: Optional[dict[str, Any]] = None,', 2))
            items.append(StringUtils.indent_str('data: Optional[Any] = None,', 2))
            items.append(StringUtils.indent_str('json: Optional[dict[str, Any] | list[Any]] = None,', 2))
            items.append(StringUtils.indent_str('requires_oauth: bool = False,', 2))
            items.append(StringUtils.indent_str('auth: HTTPBasicAuth = None,', 2))
            items.append(') -> str:')
            items.append(StringUtils.indent_str(
                'with self.session(with_oauth=requires_oauth) as session:',
                1
            ))
            items.append(StringUtils.indent_str('r: requests.Response = session.get(', 2))
            items.append(StringUtils.indent_str('url,', 3))
            items.append(StringUtils.indent_str('headers=headers,', 3))
            items.append(StringUtils.indent_str('params=params,', 3))
            items.append(StringUtils.indent_str('auth=auth,', 3))
            items.append(StringUtils.indent_str('data=data,', 3))
            items.append(StringUtils.indent_str('json=json,', 3))
            items.append(StringUtils.indent_str(')', 2))
            items.append(StringUtils.indent_str('r.raise_for_status()', 2))
            items.append(StringUtils.indent_str('return r.text', 2))
        return items

    @property
    def post_method(self) -> list[str]:
        items = []
        if self.is_async:
            items.append('async def _post(')
            items.append(StringUtils.indent_str('self,', 2))
            items.append(StringUtils.indent_str('url: str,', 2))
            items.append(StringUtils.indent_str('params: Optional[dict[str, Any]] = None,', 2))
            items.append(StringUtils.indent_str('headers: Optional[dict[str, Any]] = None,', 2))
            items.append(StringUtils.indent_str('data: Optional[Any] = None,', 2))
            items.append(StringUtils.indent_str('json: Optional[dict[str, Any] | list[Any]] = None,', 2))
            items.append(StringUtils.indent_str('requires_oauth: bool = False,', 2))
            items.append(StringUtils.indent_str('auth: BasicAuth = None,', 2))
            items.append(') -> str:')
            items.append(StringUtils.indent_str(
                'async with self.session(with_oauth=requires_oauth) as session:',
                1
            ))
            items.append(StringUtils.indent_str('async with session.post(', 2))
            items.append(StringUtils.indent_str('url,', 3))
            items.append(StringUtils.indent_str('headers=headers,', 3))
            items.append(StringUtils.indent_str('params=params,', 3))
            items.append(StringUtils.indent_str('auth=auth,', 3))
            items.append(StringUtils.indent_str('data=data,', 3))
            items.append(StringUtils.indent_str('json=json,', 3))
            items.append(StringUtils.indent_str(') as r:', 2))
            items.append(StringUtils.indent_str('return await r.text()', 3))
        else:
            items.append('def _post(')
            items.append(StringUtils.indent_str('self,', 2))
            items.append(StringUtils.indent_str('url: str,', 2))
            items.append(StringUtils.indent_str('params: Optional[dict[str, Any]] = None,', 2))
            items.append(StringUtils.indent_str('headers: Optional[dict[str, Any]] = None,', 2))
            items.append(StringUtils.indent_str('data: Optional[Any] = None,', 2))
            items.append(StringUtils.indent_str('json: Optional[dict[str, Any] | list[Any]] = None,', 2))
            items.append(StringUtils.indent_str('requires_oauth: bool = False,', 2))
            items.append(StringUtils.indent_str('auth: HTTPBasicAuth = None,', 2))
            items.append(') -> str:')
            items.append(StringUtils.indent_str(
                'with self.session(with_oauth=requires_oauth) as session:',
                1
            ))
            items.append(StringUtils.indent_str('r: requests.Response = session.post(', 2))
            items.append(StringUtils.indent_str('url,', 3))
            items.append(StringUtils.indent_str('headers=headers,', 3))
            items.append(StringUtils.indent_str('params=params,', 3))
            items.append(StringUtils.indent_str('auth=auth,', 3))
            items.append(StringUtils.indent_str('data=data,', 3))
            items.append(StringUtils.indent_str('json=json,', 3))
            items.append(StringUtils.indent_str(')', 2))
            items.append(StringUtils.indent_str('r.raise_for_status()', 2))
            items.append(StringUtils.indent_str('return r.text', 2))
        return items

    @property
    def session_context(self) -> list[str]:
        items = []
        if self.is_async:
            items.append('@asynccontextmanager')
            items.append('async def session(self, with_oauth: bool) -> Generator[ClientSession, None, None]:')
            items.append(StringUtils.indent_str('headers = {', 1))
            items.append(StringUtils.indent_str('\'X-API-Key\': self.api_key,', 2))
            items.append(StringUtils.indent_str('\'User-Agent\': \'bungie-api-python\'', 2))
            items.append(StringUtils.indent_str('}', 1))
            items.append(StringUtils.indent_str('if with_oauth:', 1))
            items.append(StringUtils.indent_str('headers.update({', 2))
            items.append(StringUtils.indent_str('\'Authorization\': self.oauth_context()', 3))
            items.append(StringUtils.indent_str('})', 2))
            items.append('')
            items.append(StringUtils.indent_str('async with ClientSession(', 1))
            items.append(StringUtils.indent_str('headers=headers,', 3))
            items.append(StringUtils.indent_str('raise_for_status=True,', 3))
            items.append(StringUtils.indent_str(') as session:', 1))
            items.append(StringUtils.indent_str('yield session', 2))
        else:
            items.append('@contextmanager')
            items.append('def session(self, with_oauth: bool) -> Generator[Session, None, None]:')
            items.append(StringUtils.indent_str('with Session() as session:', 1))
            items.append(StringUtils.indent_str('session.headers.update({', 2))
            items.append(StringUtils.indent_str('\'X-API-Key\': self.api_key,', 3))
            items.append(StringUtils.indent_str('\'User-Agent\': \'bungie-api-python\'', 3))
            items.append(StringUtils.indent_str('})', 2))
            items.append(StringUtils.indent_str('if with_oauth:', 2))
            items.append(StringUtils.indent_str('session.headers.update({', 3))
            items.append(StringUtils.indent_str('\'Authorization\': self.oauth_context()', 4))
            items.append(StringUtils.indent_str('})', 3))
            items.append('')
            items.append(StringUtils.indent_str('yield session', 2))
        return items

    @property
    def text_content(self) -> str:
        content = self.imports.formatted_imports
        content += '\n'
        content += StringUtils.gen_line_break_comment('CLIENT DEFINITION')
        content += '\n'
        content += StringUtils.gen_class_declaration(self.name)
        content += '\n'
        content += StringUtils.indent_str('def __init__(self, api_key: str):\n', 1)
        content += StringUtils.indent_str('if not api_key:\n', 2)
        content += StringUtils.indent_str('raise ValueError(\'You must provide a valid API key.\')\n', 3)
        content += '\n'
        content += StringUtils.indent_str('self.api_key = api_key\n', 2)
        content += '\n'
        content += '\n'.join(
            StringUtils.indent_str(f'self.{e.var_name} = {e.name_async if self.is_async else e.name_sync}(self)', 2)
            for e in self.endpoints
        )
        content += '\n\n'
        content += '\n'.join(StringUtils.indent_str(s, 1) for s in self.session_context)
        content += '\n\n'
        content += '\n'.join(StringUtils.indent_str(s, 1) for s in self.get_method)
        content += '\n\n'
        content += '\n'.join(StringUtils.indent_str(s, 1) for s in self.post_method)
        content += '\n'
        return content

    @property
    def file_name(self) -> str:
        if self.is_async:
            return self.async_client_file_name
        else:
            return self.sync_client_file_name

    @property
    def name(self) -> str:
        if self.is_async:
            return self.async_client_name
        else:
            return self.sync_client_name

    def write_file(self, folder: str) -> None:
        with open(os.path.join(folder, self.file_name + self.file_extension), 'w+') as cl:
            cl.write(self.text_content)
