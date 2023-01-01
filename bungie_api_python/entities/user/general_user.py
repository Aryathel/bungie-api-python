from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json

from .user_to_user_context import UserToUserContext
from ..model_utils import datetime_metadata


@dataclass_json
@dataclass(kw_only=True)
class GeneralUser:
    membershipId: int
    uniqueName: str
    normalizedName: Optional[str] = field(default=None)
    displayName: str
    profilePicture: int
    profileTheme: int
    userTitle: int
    successMessageFlags: int
    isDeleted: bool
    about: str
    firstAccess: Optional[datetime] = field(
        default=None,
        metadata=datetime_metadata
    )
    lastUpdate: Optional[datetime] = field(
        default=None,
        metadata=datetime_metadata
    )
    legacyPortalUID: Optional[int] = field(default=None)
    context: Optional[UserToUserContext] = field(default=None)
    psnDisplayName: Optional[str] = field(default=None)
    xboxDisplayName: Optional[str] = field(default=None)
    fbDisplayName: Optional[str] = field(default=None)
    showActivity: Optional[bool] = field(default=None)
    locale: str
    localeInheritDefault: bool
    lastBanReportId: Optional[int] = field(default=None)
    showGroupMessaging: bool
    profilePicturePath: str
    profilePictureWidePath: Optional[str] = field(default=None)
    profileThemeName: str
    userTitleDisplay: str
    statusText: str
    statusDate: datetime = field(
        metadata=datetime_metadata
    )
    profileBanExpire: Optional[datetime] = field(
        default=None,
        metadata=datetime_metadata
    )
    blizzardDisplayName: Optional[str] = field(default=None)
    steamDisplayName: Optional[str] = field(default=None)
    stadiaDisplayName: Optional[str] = field(default=None)
    twitchDisplayName: Optional[str] = field(default=None)
    cachedBungieGlobalDisplayName: Optional[str] = field(default=None)
    cachedBungieGlobalDisplayNameCode: Optional[int] = field(default=None)
    egsDisplayName: Optional[str] = field(default=None)
