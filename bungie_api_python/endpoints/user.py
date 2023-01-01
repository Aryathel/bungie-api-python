from ..endpoint_base import EndpointBase
from ..entities.responses.user import GetBungieNetUserById, GetSanitizedPlatformDisplayNames, \
    GetCredentialTypesForTargetAccount


class UserEndpoints(EndpointBase, api_base='https://www.bungie.net/Platform/User', name='user'):
    def get_bungie_net_user_by_id(self, id: int) -> GetBungieNetUserById:
        return self.parent.get(
            f'{self.api_base}/GetBungieNetUserById/{id}/',
            response_type=GetBungieNetUserById,
        )

    def get_sanitized_platform_display_names(self, membership_id: int) -> GetSanitizedPlatformDisplayNames:
        return self.parent.get(
            f'{self.api_base}/GetSanitizedPlatformDisplayNames/{membership_id}/',
            response_type=GetSanitizedPlatformDisplayNames,
        )

    def get_credential_types_for_target_account(self, membership_id: int) -> GetCredentialTypesForTargetAccount:
        return self.parent.get(
            f'{self.api_base}/GetCredentialTypesForTargetAccount/{membership_id}',
            response_type=GetCredentialTypesForTargetAccount,
            requires_oauth=True,
        )


class UserEndpointsAsync(EndpointBase, api_base='https://www.bungie.net/Platform/User', name='user'):
    async def get_bungie_net_user_by_id(self, id: int) -> GetBungieNetUserById:
        return await self.parent.get(
            f'{self.api_base}/GetBungieNetUserById/{id}/',
            response_type=GetBungieNetUserById,
        )

    async def get_sanitized_platform_display_names(self, membership_id: int) -> GetSanitizedPlatformDisplayNames:
        return await self.parent.get(
            f'{self.api_base}/GetSanitizedPlatformDisplayNames/{membership_id}/',
            response_type=GetSanitizedPlatformDisplayNames,
        )

    async def get_credential_types_for_target_account(self, membership_id: int) -> GetCredentialTypesForTargetAccount:
        return await self.parent.get(
            f'{self.api_base}/GetCredentialTypesForTargetAccount/{membership_id}',
            response_type=GetCredentialTypesForTargetAccount,
            requires_oauth=True,
        )
