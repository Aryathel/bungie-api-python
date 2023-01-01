from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .user_search_response_detail import UserSearchResponseDetail


@dataclass_json
@dataclass(kw_only=True)
class UserSearchResponse:
    searchResults: list[UserSearchResponseDetail]
    page: int
    hasMore: bool
