from ..endpoint_base import EndpointBase
from ..entities.core import BungieMembershipType, BungieCredentialType
from ..entities.responses import GetBungieNetUserById, GetSanitizedPlatformDisplayNames, \
    GetCredentialTypesForTargetAccount, GetAvailableThemes, GetMembershipDataById, GetMembershipDataForCurrentUser, \
    GetMembershipFromHardLinkedCredential


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

    def get_available_themes(self) -> GetAvailableThemes:
        return self.parent.get(
            f'{self.api_base}/GetAvailableThemes/',
            response_type=GetAvailableThemes,
        )

    def get_membership_data_by_id(
            self,
            membership_id: int,
            membership_type: BungieMembershipType | int
    ) -> GetMembershipDataById:
        if not isinstance(membership_type, BungieMembershipType):
            membership_type = BungieMembershipType(membership_type)

        return self.parent.get(
            f'{self.api_base}/GetMembershipsById/{membership_id}/{membership_type.value}/',
            response_type=GetMembershipDataById,
        )

    def get_membership_data_for_current_user(self) -> GetMembershipDataForCurrentUser:
        return self.parent.get(
            f'{self.api_base}/GetMembershipsForCurrentUser/',
            response_type=GetMembershipDataForCurrentUser,
            requires_oauth=True
        )

    def get_membership_from_hard_linked_credential(
            self,
            credential_type: BungieCredentialType | int | str,
            credential: int | str,
    ) -> GetMembershipFromHardLinkedCredential:
        if isinstance(credential_type, int):
            credential_type = BungieCredentialType(credential_type)
        elif isinstance(credential_type, str):
            for cr_type in BungieCredentialType:
                if cr_type.name == credential_type:
                    credential_type = cr_type

        if not isinstance(credential_type, BungieCredentialType):
            raise ValueError(f'The credential type "{credential_type}" is not a valid BungieCredentialType.')

        return self.parent.get(
            f'{self.api_base}/GetMembershipFromHardLinkedCredential/{credential_type.name}/{credential}/',
            response_type=GetMembershipFromHardLinkedCredential,
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

    async def get_available_themes(self) -> GetAvailableThemes:
        return await self.parent.get(
            f'{self.api_base}/GetAvailableThemes/',
            response_type=GetAvailableThemes,
        )

    async def get_membership_data_by_id(
            self,
            membership_id: int,
            membership_type: BungieMembershipType | int
    ) -> GetMembershipDataById:
        if not isinstance(membership_type, BungieMembershipType):
            membership_type = BungieMembershipType(membership_type)

        return await self.parent.get(
            f'{self.api_base}/GetMembershipsById/{membership_id}/{membership_type.value}/',
            response_type=GetMembershipDataById,
        )

    async def get_membership_data_for_current_user(self) -> GetMembershipDataForCurrentUser:
        return await self.parent.get(
            f'{self.api_base}/GetMembershipsForCurrentUser/',
            response_type=GetMembershipDataForCurrentUser,
            requires_oauth=True
        )

    async def get_membership_from_hard_linked_credential(
            self,
            credential_type: BungieCredentialType | int | str,
            credential: int | str,
    ) -> GetMembershipFromHardLinkedCredential:
        if isinstance(credential_type, int):
            credential_type = BungieCredentialType(credential_type)
        elif isinstance(credential_type, str):
            for cr_type in BungieCredentialType:
                if cr_type.name == credential_type:
                    credential_type = cr_type

        if not isinstance(credential_type, BungieCredentialType):
            raise ValueError(f'The credential type "{credential_type}" is not a valid BungieCredentialType.')

        return await self.parent.get(
            f'{self.api_base}/GetMembershipFromHardLinkedCredential/{credential_type.name}/{credential}/',
            response_type=GetMembershipFromHardLinkedCredential,
        )
