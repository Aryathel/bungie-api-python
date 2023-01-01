from ..endpoint_base import EndpointBase
from ..entities.responses.user import GetBungieNetUserById


class UserEndpoints(EndpointBase, api_base='https://www.bungie.net/Platform/User', name='user'):
    def get_bungie_net_user_by_id(self, id: int) -> GetBungieNetUserById:
        return self.parent.get(
            f'{self.api_base}/GetBungieNetUserById/{id}/',
            response_type=GetBungieNetUserById,
        )


class UserEndpointsAsync(EndpointBase, api_base='https://www.bungie.net/Platform/User', name='user'):
    async def get_bungie_net_user_by_id(self, id: int) -> GetBungieNetUserById:
        return await self.parent.get(
            f'{self.api_base}/GetBungieNetUserById/{id}/',
            response_type=GetBungieNetUserById,
        )
