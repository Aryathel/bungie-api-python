from enum import Enum


class BungieMembershipType(Enum):
    None_ = 0
    TigerXbox = 1
    TigerPsn = 2
    TigerSteam = 3
    TigerBlizzard = 4
    TigerStadia = 5
    TigerEgs = 6
    TigerDemon = 10
    BungieNext = 254
    All = -1


class OAuthClientType(Enum):
    NotApplicable = 0
    Public = 1
    Confidential = 2
