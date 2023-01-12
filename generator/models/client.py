import os

from .endpoints import EndpointCollection
from .entity_import import EntityImportCollection, EntityImport
from .enums import ImportType
from ..utils.str_utils import StringUtils


class Client:
    utils_path_name = 'utils'
    oauth_util_name = 'oauth_utils'
    endpoints_path_name = 'endpoints'
    sync_client_name = 'BungieClientSync'
    async_client_name = 'BungieClientAsync'
    sync_client_file_name = 'client_sync'
    async_client_file_name = 'client_async'
    file_extension = '.py'

    def __init__(
            self,
            is_async: bool,
            api_key_var: str,
            api_key_header: str,
            oauth_url: str,
            endpoints: list[EndpointCollection]
    ):
        self.is_async = is_async
        self.endpoints = endpoints
        self.api_key_var = api_key_var
        self.api_key_header = api_key_header
        self.oauth_url = oauth_url

        self.imports = EntityImportCollection([
            EntityImport(
                name='typing',
                type=ImportType.stdlib,
                imports=['Optional', 'Any', 'Generator']
            ),
            EntityImport(
                name=f'{self.utils_path_name}.{self.oauth_util_name}',
                type=ImportType.relative,
                imports=[
                    'OAuthClientType',
                    'AccessToken',
                    'OAuthInformationNotProvided',
                    'OAuthContextExpired',
                    'OAuthContextNotFound',
                    'OAuthInitFailure',
                ]
            ),
            EntityImport(name='datetime', type=ImportType.stdlib, imports=['datetime']),
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
                imports=['BasicAuth', 'ClientSession', 'ClientResponseError']
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
                imports=['Session', 'HTTPError']
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
                'async with self.session(requires_oauth=requires_oauth) as session:',
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
                'with self.session(requires_oauth=requires_oauth) as session:',
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
                'async with self.session(requires_oauth=requires_oauth) as session:',
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
                'with self.session(requires_oauth=requires_oauth) as session:',
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
        if self.is_async:
            return [
                '@asynccontextmanager',
                'async def session(self, requires_oauth: bool) -> Generator[ClientSession, None, None]:',
                StringUtils.indent_str('headers = {', 1),
                StringUtils.indent_str(f'\'{self.api_key_header}\': self.{self.api_key_var},', 2),
                StringUtils.indent_str('\'User-Agent\': \'bungie-api-python\'', 2),
                StringUtils.indent_str('}', 1),
                StringUtils.indent_str('if requires_oauth or self.has_oauth:', 1),
                StringUtils.indent_str('headers.update({', 2),
                StringUtils.indent_str('\'Authorization\': self.oauth_context()', 3),
                StringUtils.indent_str('})', 2), '',
                StringUtils.indent_str('async with ClientSession(', 1),
                StringUtils.indent_str('headers=headers,', 3),
                StringUtils.indent_str('raise_for_status=True,', 3),
                StringUtils.indent_str(') as session:', 1),
                StringUtils.indent_str('yield session', 2)
            ]
        else:
            return [
                '@contextmanager',
                'def session(self, requires_oauth: bool) -> Generator[Session, None, None]:',
                StringUtils.indent_str('with Session() as session:', 1),
                StringUtils.indent_str('session.headers.update({', 2),
                StringUtils.indent_str(f'\'{self.api_key_header}\': self.{self.api_key_var},', 3),
                StringUtils.indent_str('\'User-Agent\': \'bungie-api-python\'', 3),
                StringUtils.indent_str('})', 2),
                StringUtils.indent_str('if requires_oauth or self.has_oauth:', 2),
                StringUtils.indent_str('session.headers.update({', 3),
                StringUtils.indent_str('\'Authorization\': self.oauth_context()', 4),
                StringUtils.indent_str('})', 3), '',
                StringUtils.indent_str('yield session', 2)
            ]

    @property
    def init_method(self) -> list[str]:
        items = [
            StringUtils.gen_function_declaration(
                '__init__',
                [
                    'self',
                    f'{self.api_key_var}: str',
                    'client_id: Optional[int] = None',
                    'client_secret: Optional[str] = None'
                ],
                'None',
            ),
            StringUtils.indent_str(f'if not {self.api_key_var}:', 1),
            StringUtils.indent_str('raise ValueError(\'You must provide a valid API key.\')\n', 2),
            StringUtils.indent_str(f'self.{self.api_key_var} = {self.api_key_var}', 1),
            StringUtils.indent_str(f'self.client_id = client_id', 1),
            StringUtils.indent_str(f'self.client_secret = client_secret\n', 1)
        ]
        for e in self.endpoints:
            items.append(StringUtils.indent_str(
                f'self.{e.var_name} = {e.name_async if self.is_async else e.name_sync}(self)',
                1
            ))
        items.append('')
        items.append(StringUtils.indent_str('self._access_token = None', 1))
        return items

    @property
    def oauth_type_property(self) -> list[str]:
        return [
            '@property',
            'def oauth_type(self) -> OAuthClientType:',
            StringUtils.indent_str('if self.client_id:', 1),
            StringUtils.indent_str('if self.client_secret:', 2),
            StringUtils.indent_str('return OAuthClientType.Confidential', 3),
            StringUtils.indent_str('else:', 2),
            StringUtils.indent_str('return OAuthClientType.Public', 3),
            StringUtils.indent_str('else:', 1),
            StringUtils.indent_str('return OAuthClientType.NotApplicable', 2)
        ]

    @property
    def oauth_context_method(self) -> list[str]:
        items = [
            StringUtils.gen_function_declaration('oauth_context', ['self'], 'str', is_async=self.is_async),
            StringUtils.indent_str('if self.oauth_type == OAuthClientType.NotApplicable:', 1),
            StringUtils.indent_str('raise OAuthInformationNotProvided(', 2),
            StringUtils.indent_str(
                '"You must provide a \'client_id\' and optionally a \'client_secret\' \"',
                3,
            ),
            StringUtils.indent_str('"to the client in order to use OAuth endpoints."', 3),
            StringUtils.indent_str(')\n', 2),
            StringUtils.gen_comment('OAuth access token not set', 1),
            StringUtils.indent_str('if not self.has_oauth:', 1),
            StringUtils.indent_str('raise OAuthContextNotFound(', 2),
            StringUtils.indent_str(
                '"No OAuth context was found. '
                'Use the client\'s \'oauth_init\' method to establish a new OAuth context."',
                3
            ),
            StringUtils.indent_str(')\n', 2),
            StringUtils.gen_comment('OAuth access token is expired', 1),
            StringUtils.indent_str('if self._access_token.is_expired:', 1),
            StringUtils.indent_str('if self._access_token.is_refresh_expired:', 2),
            StringUtils.indent_str('raise OAuthContextExpired(', 3),
            StringUtils.indent_str('"The previous OAuth context has expired and cannot be refreshed. "', 4),
            StringUtils.indent_str('"Please reset the oauth context using the client\'s \'oauth_init\' method."', 4),
            StringUtils.indent_str(')\n', 3),
            StringUtils.indent_str('try:', 2),
        ]
        if self.is_async:
            items += [
                StringUtils.indent_str(
                    'self._access_token = await self.oauth.refresh_access_token(self._access_token.refresh_token)',
                    3
                ),
                StringUtils.indent_str('except ClientResponseError:', 2),
            ]
        else:
            items += [
                StringUtils.indent_str(
                    'self._access_token = self.oauth.refresh_access_token(self._access_token.refresh_token)',
                    3
                ),
                StringUtils.indent_str('except HTTPError:', 2),
            ]

        items += [
            StringUtils.indent_str('raise OAuthContextExpired(', 3),
            StringUtils.indent_str('"The previous OAuth context has expired and cannot be refreshed. "', 4),
            StringUtils.indent_str('"Please reset the oauth context using the client\'s \'oauth_init\' method."', 4),
            StringUtils.indent_str(')\n', 3),
            StringUtils.indent_str('return self._access_token.header', 2)
        ]
        return items

    @property
    def oauth_init_method(self) -> list[str]:
        items = [
            'async def oauth_init(' if self.is_async else 'def oauth_init(',
            StringUtils.indent_str('self,', 2),
            StringUtils.indent_str('code: Optional[str] = None,', 2),
            StringUtils.indent_str('access_token: Optional[str] = None,', 2),
            StringUtils.indent_str('access_token_expires: Optional[datetime] = None,', 2),
            StringUtils.indent_str('refresh_token: Optional[str] = None,', 2),
            StringUtils.indent_str('refresh_token_expires: Optional[datetime] = None,', 2),
            StringUtils.indent_str('token_type: Optional[str] = \'Bearer\',', 2),
            ') -> None:',
            StringUtils.indent_str('if code:', 1),
            StringUtils.indent_str('try:', 2),
        ]
        if self.is_async:
            items += [
                StringUtils.indent_str('self._access_token = await self.oauth.get_access_token(code)', 3),
                StringUtils.indent_str('except ClientResponseError:', 2)
            ]
        else:
            items += [
                StringUtils.indent_str('self._access_token = self.oauth.get_access_token(code)', 3),
                StringUtils.indent_str('except HTTPError:', 2)
            ]
        items += [
            StringUtils.indent_str(
                'raise OAuthInitFailure("Failed to establish an OAuth context with the provided authorization code.")',
                3
            ),
            StringUtils.indent_str('else:', 1),
            StringUtils.indent_str('if not access_token or not access_token_expires:', 2),
            StringUtils.indent_str('raise OAuthInitFailure(', 3),
            StringUtils.indent_str('"Either an authorization code, "', 4),
            StringUtils.indent_str('"or an existing access token and expiration timestamp must be provided."', 4),
            StringUtils.indent_str(')', 3),
            StringUtils.indent_str('elif not token_type or not isinstance(token_type, str):', 2),
            StringUtils.indent_str(
                'raise OAuthInitFailure("A valid token_type must be passed. '
                'This is most likely meant to be \'Bearer\'.")\n',
                3
            ),
            StringUtils.indent_str('self._access_token = AccessToken(', 2),
            StringUtils.indent_str('access_token=access_token,', 3),
            StringUtils.indent_str('token_type=token_type,', 3),
            StringUtils.indent_str('expires_in=int((access_token_expires - datetime.utcnow()).total_seconds()),', 3),
            StringUtils.indent_str('refresh_token=refresh_token,', 3),
            StringUtils.indent_str('refresh_expires_in=(', 3),
            StringUtils.indent_str('int((refresh_token_expires - datetime.utcnow()).total_seconds())', 4),
            StringUtils.indent_str('if refresh_token_expires else None', 4),
            StringUtils.indent_str('),', 3),
            StringUtils.indent_str(')', 2),
        ]
        return items

    @property
    def has_oauth_property(self) -> list[str]:
        return [
            '@property',
            'def has_oauth(self) -> bool:',
            StringUtils.indent_str('return bool(self._access_token)', 1)
        ]

    @property
    def authorization_url_property(self) -> list[str]:
        return [
            '@property',
            'def authorization_url(self) -> Optional[str]:',
            StringUtils.indent_str('if not self.oauth_type == OAuthClientType.NotApplicable:', 1),
            StringUtils.indent_str(f'return f\'{self.oauth_url}?client_id={{self.client_id}}&response_type=code\'', 2),
            StringUtils.indent_str('return None', 1),
        ]

    @property
    def text_content(self) -> str:
        content = self.imports.formatted_imports
        content += '\n'
        content += StringUtils.gen_line_break_comment('CLIENT DEFINITION')
        content += '\n'
        content += StringUtils.gen_class_declaration(self.name)
        content += '\n'
        content += StringUtils.indent_str('_access_token: Optional[AccessToken]', 1)
        content += '\n\n'
        content += '\n'.join(StringUtils.indent_str(s, 1) for s in self.init_method)
        content += '\n\n'
        content += '\n'.join(StringUtils.indent_str(s, 1) for s in self.oauth_type_property)
        content += '\n\n'
        content += '\n'.join(StringUtils.indent_str(s, 1) for s in self.has_oauth_property)
        content += '\n\n'
        content += '\n'.join(StringUtils.indent_str(s, 1) for s in self.authorization_url_property)
        content += '\n\n'
        content += '\n'.join(StringUtils.indent_str(s, 1) for s in self.session_context)
        content += '\n\n'
        content += '\n'.join(StringUtils.indent_str(s, 1) for s in self.oauth_context_method)
        content += '\n\n'
        content += '\n'.join(StringUtils.indent_str(s, 1) for s in self.oauth_init_method)
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
