from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json

from ...utils import OAuthUtils


@dataclass_json
@dataclass(kw_only=True)
class AccessToken:
    # Standard Bungie fields.
    access_token: str
    token_type: str
    expires_in: int
    # Public OAuth applications do not include refresh information.
    refresh_token: Optional[str] = field(default=None)
    refresh_expires_in: Optional[int] = field(default=None)
    membership_id: int

    # Custom helper fields.
    expires_at: Optional[datetime] = field(default=None)
    refresh_expires_at: Optional[datetime] = field(default=None)

    def __post_init__(self):
        self.expires_at = OAuthUtils.access_token_expire_date_utc(self)
        if self.refresh_expires_in:
            self.refresh_expires_at = OAuthUtils.refresh_token_expire_date_utc(self)
