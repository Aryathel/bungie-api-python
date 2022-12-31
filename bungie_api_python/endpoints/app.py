from ..endpoint_base import EndpointBase
from ..entities.responses.app import GetBungieApplications


class AppEndpoints(EndpointBase, api_base="https://bungie.net/Platform/App", name="app"):
    def get_bungie_applications(self) -> GetBungieApplications:
        return self.parent.get(f'{self.api_base}/FirstParty', response_type=GetBungieApplications)


class AppEndpointsAsync(EndpointBase, api_base="https://bungie.net/Platform/App", name="app"):
    async def get_bungie_applications(self) -> GetBungieApplications:
        return await self.parent.get(f'{self.api_base}/FirstParty', response_type=GetBungieApplications)
