from enum import Flag, Enum


class ApplicationScopes(Flag):
    ReadBasicUserProfile = 1
    ReadGroups = 2
    WriteGroups = 4
    AdminGroups = 8
    BnetWrite = 16
    MoveEquipDestinyItems = 32
    ReadDestinyInventoryAndVault = 64
    ReadUserData = 128
    EditUserData = 256
    ReadDestinyVendorsAndAdvisors = 512
    ReadAndApplyTokens = 1024
    AdvancedWriteActions = 2048
    PartnerOfferGrant = 4096
    DestinyUnlockValueQuery = 8192
    UserPiiRead = 16384


class ApplicationStatus(Enum):
    None_ = 0
    Private = 1
    Public = 2
    Disabled = 3
    Blocked = 4


class DeveloperRole(Enum):
    None_ = 0
    Owner = 1
    TeamMember = 2
