from datetime import datetime
from typing import Optional

from ..endpoint_base import EndpointBase
from ..entities.responses.app import GetBungieApplications, GetApplicationApiUsage
from ..utils.datetimes import DateTimeUtils


class AppEndpoints(EndpointBase, api_base="https://www.bungie.net/Platform/App", name="app"):
    def get_application_api_usage(
            self,
            application_id: int,
            end: Optional[datetime] = None,
            start: Optional[datetime] = None,
    ) -> GetApplicationApiUsage:
        params = None
        if end or start:
            params = {}
        if end:
            params['end'] = DateTimeUtils.encode_datetime(end)
        if start:
            params['start'] = DateTimeUtils.encode_datetime(start)

        return self.parent.get(
            f'{self.api_base}/ApiUsage/{application_id}',
            response_type=GetApplicationApiUsage,
            params=params,
            requires_oauth=True,
        )

    def get_bungie_applications(self) -> GetBungieApplications:
        return self.parent.get(f'{self.api_base}/FirstParty', response_type=GetBungieApplications)


class AppEndpointsAsync(EndpointBase, api_base="https://www.bungie.net/Platform/App", name="app"):
    async def get_application_api_usage(
            self,
            application_id: int,
            end: Optional[datetime] = None,
            start: Optional[datetime] = None,
    ) -> GetApplicationApiUsage:
        params = None
        if end or start:
            params = {}
        if end:
            params['end'] = DateTimeUtils.encode_datetime(end)
        if start:
            params['start'] = DateTimeUtils.encode_datetime(start)

        return await self.parent.get(
            f'{self.api_base}/ApiUsage/{application_id}',
            response_type=GetApplicationApiUsage,
            params=params,
            requires_oauth=True,
        )

    async def get_bungie_applications(self) -> GetBungieApplications:
        return await self.parent.get(f'{self.api_base}/FirstParty', response_type=GetBungieApplications)
