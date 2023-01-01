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


class BungieCredentialType(Enum):
    None_ = 0
    Xuid = 1
    Psnid = 2
    Wlid = 3
    Fake = 4
    Facebook = 5
    Google = 8
    Windows = 9
    DemonId = 10
    SteamId = 12
    BattleNetId = 14
    StadiaId = 16
    TwitchId = 18
    EgsId = 20


class OAuthClientType(Enum):
    NotApplicable = 0
    Public = 1
    Confidential = 2
