# Bungie API Python Wrapper

This is a work in progress python wrapper for the Bungie API.

[MIT License](LICENSE.md)

[Test Status](tests/README.md)


## Planned Features

- [ ] Complete API coverage.
  - [x] OAuth workflow
    - [x] Token endpoints (access token, refresh token)
    - [x] OAuth context for endpoints requiring it.
  - [ ] Endpoints
    - [x] App
    - [x] User
    - [ ] Content
    - [ ] Forum
    - [ ] GroupV2
    - [ ] Tokens
    - [ ] Destiny2
    - [ ] CommunityContent
    - [ ] Trending
    - [ ] Fireteam
    - [ ] Social
    - [ ] Common
  - [ ] Entity Models
- [x] Async and sync client implementations.

## Endpoints

### OAuth Endpoints

| Endpoint        | Implemented        | Tested             | Comments |
|-----------------|--------------------|--------------------|----------|
| GetAccessToken  | :heavy_check_mark: | :heavy_check_mark: |          |
| GetRefreshToken | :heavy_check_mark: | :heavy_check_mark: |          |

### App Endpoints

| Endpoint               | Implemented        | Tested             | Comments |
|------------------------|--------------------|--------------------|----------|
| GetApplicationApiUsage | :heavy_check_mark: | :heavy_check_mark: |          |
| GetBungieApplications  | :heavy_check_mark: | :heavy_check_mark: |          |

### User Endpoints

| Endpoint                              | Implemented        | Tested             | Comments                                                                                               |
|---------------------------------------|--------------------|--------------------|--------------------------------------------------------------------------------------------------------|
| GetBungieNetUserById                  | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |
| GetSanitizedPlatformDisplayNames      | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |
| GetCredentialTypesForTargetAccount    | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |
| GetAvailableThemes                    | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |
| GetMembershipDataById                 | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |
| GetMembershipDataForCurrentUser       | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |
| GetMembershipFromHardLinkedCredential | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |
| SearchByGlobalNamePrefix              | :x:                | :x:                | This endpoint is obsolete and will raise an error if called, it is only included for posterity's sake. |
| SearchByGlobalNamePost                | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |

### Content Endpoints

| Endpoint                  | Implemented | Tested | Comments |
|---------------------------|-------------|--------|----------|
| GetContentType            | :x:         | :x:    |          |
| GetContentById            | :x:         | :x:    |          |
| GetContentByTagAndType    | :x:         | :x:    |          |
| SearchContentWithText     | :x:         | :x:    |          |
| SearchContentByTagAndType | :x:         | :x:    |          |
| SearchHelpArticles        | :x:         | :x:    |          |
| RssNewsArticles           | :x:         | :x:    |          |

### Forum Endpoints

| Endpoint                         | Implemented | Tested | Comments |
|----------------------------------|-------------|--------|----------|
| GetTopicsPaged                   | :x:         | :x:    |          |
| GetCoreTopicsPaged               | :x:         | :x:    |          |
| GetPostsThreadedPaged            | :x:         | :x:    |          |
| GetPostsThreadedPagedFromChild   | :x:         | :x:    |          |
| GetPostAndParent                 | :x:         | :x:    |          |
| GetPostAndParentAwaitingApproval | :x:         | :x:    |          |
| GetTopicForContent               | :x:         | :x:    |          |
| GetForumTagSuggestions           | :x:         | :x:    |          |
| GetPoll                          | :x:         | :x:    |          |
| GetRecruitmentThreadSummaries    | :x:         | :x:    |          |


### GroupV2 Endpoints

| Endpoint                      | Implemented | Tested | Comments |
|-------------------------------|-------------|--------|----------|
| GetAvailableAvatars           | :x:         | :x:    |          |
| GetAvailableThemes            | :x:         | :x:    |          |
| GetUserClanInviteSetting      | :x:         | :x:    |          |
| GetRecommendedGroups          | :x:         | :x:    |          |
| GroupSearch                   | :x:         | :x:    |          |
| GetGroup                      | :x:         | :x:    |          |
| GetGroupByName                | :x:         | :x:    |          |
| GetGroupByNameV2              | :x:         | :x:    |          |
| GetGroupOptionalConversations | :x:         | :x:    |          |
| EditGroup                     | :x:         | :x:    |          |
| EditClanBanner                | :x:         | :x:    |          |
| EditFounderOptions            | :x:         | :x:    |          |
| AddOptionalConversation       | :x:         | :x:    |          |
| EditOptionalConversation      | :x:         | :x:    |          |
| GetMembersOfGroup             | :x:         | :x:    |          |
| GetAdminsAndFounderOfGroup    | :x:         | :x:    |          |
| EditGroupMembership           | :x:         | :x:    |          |
| KickMember                    | :x:         | :x:    |          |
| BanMember                     | :x:         | :x:    |          |
| UnbanMember                   | :x:         | :x:    |          |
| GetBannedMembersOfGroup       | :x:         | :x:    |          |
| AbdicateFoundership           | :x:         | :x:    |          |
| GetPendingMemberships         | :x:         | :x:    |          |
| GetInvitedIndividuals         | :x:         | :x:    |          |
| ApproveAllPending             | :x:         | :x:    |          |
| DenyAllPending                | :x:         | :x:    |          |
| ApprovePendingForList         | :x:         | :x:    |          |
| ApprovePending                | :x:         | :x:    |          |
| DenyPendingForList            | :x:         | :x:    |          |
| GetGroupsForMember            | :x:         | :x:    |          |
| RecoverGroupForFounder        | :x:         | :x:    |          |
| GetPotentialGroupsForMember   | :x:         | :x:    |          |
| IndividualGroupInvite         | :x:         | :x:    |          |
| IndividualGroupInviteCancel   | :x:         | :x:    |          |


### Tokens Endpoints

| Endpoint                              | Implemented | Tested | Comments |
|---------------------------------------|-------------|--------|----------|
| ForceDropsRepair                      | :x:         | :x:    |          |
| ClaimPartnerOffer                     | :x:         | :x:    |          |
| ApplyMissingPartnerOffersWithoutClaim | :x:         | :x:    |          |
| GetPartnerOfferSkuHistory             | :x:         | :x:    |          |
| GetPartnerRewardHistory               | :x:         | :x:    |          |
| GetBungieRewardsForUser               | :x:         | :x:    |          |
| GetBungieRewardsForPlatformUser       | :x:         | :x:    |          |
| GetBungieRewardsList                  | :x:         | :x:    |          |


### Destiny2 Endpoints

| Endpoint                                   | Implemented | Tested | Comments |
|--------------------------------------------|-------------|--------|----------|
| GetDestinyManifest                         | :x:         | :x:    |          |
| GetDestinyEntityDefinition                 | :x:         | :x:    |          |
| SearchDestinyPlayerByBungieName            | :x:         | :x:    |          |
| GetLinkedProfiles                          | :x:         | :x:    |          |
| GetProfile                                 | :x:         | :x:    |          |
| GetCharacter                               | :x:         | :x:    |          |
| GetClanWeeklyRewardState                   | :x:         | :x:    |          |
| GetClanBannerSource                        | :x:         | :x:    |          |
| GetItem                                    | :x:         | :x:    |          |
| GetVendors                                 | :x:         | :x:    |          |
| GetVendor                                  | :x:         | :x:    |          |
| GetPublicVendors                           | :x:         | :x:    |          |
| GetCollectibleNodeDetails                  | :x:         | :x:    |          |
| TransferItem                               | :x:         | :x:    |          |
| PullFromPostmaster                         | :x:         | :x:    |          |
| EquipItem                                  | :x:         | :x:    |          |
| EquipItems                                 | :x:         | :x:    |          |
| SetItemLockState                           | :x:         | :x:    |          |
| SetQuestTrackedState                       | :x:         | :x:    |          |
| InsertSocketPlug                           | :x:         | :x:    |          |
| InsertSocketPlugFree                       | :x:         | :x:    |          |
| GetPostGameCarnageReport                   | :x:         | :x:    |          |
| ReportOffensivePostGameCarnageReportPlayer | :x:         | :x:    |          |
| GetHistoricalStatsDefinition               | :x:         | :x:    |          |
| GetClanLeaderboards                        | :x:         | :x:    |          |
| GetClanAggregateStats                      | :x:         | :x:    |          |
| GetLeaderboards                            | :x:         | :x:    |          |
| GetLeaderboardsForCharacter                | :x:         | :x:    |          |
| SearchDestinyEntities                      | :x:         | :x:    |          |
| GetHistoricalStats                         | :x:         | :x:    |          |
| GetHistoricalStatsForAccount               | :x:         | :x:    |          |
| GetActivityHistory                         | :x:         | :x:    |          |
| GetUniqueWeaponHistory                     | :x:         | :x:    |          |
| GetDestinyAggregateActivityStats           | :x:         | :x:    |          |
| GetPublicMilestoneContent                  | :x:         | :x:    |          |
| GetPublicMilestones                        | :x:         | :x:    |          |
| AwaInitializeRequest                       | :x:         | :x:    |          |
| AwaProvideAuthorizationResult              | :x:         | :x:    |          |
| AwaGetActionToken                          | :x:         | :x:    |          |


### CommunityContent Endpoint

| Endpoint            | Implemented | Tested | Comments |
|---------------------|-------------|--------|----------|
| GetCommunityContent | :x:         | :x:    |          |


### Trending Endpoints

| Endpoint               | Implemented | Tested | Comments |
|------------------------|-------------|--------|----------|
| GetTrendingCategories  | :x:         | :x:    |          |
| GetTrendingCategory    | :x:         | :x:    |          |
| GetTrendingEntryDetail | :x:         | :x:    |          |


### Fireteam Endpoints

| Endpoint                           | Implemented | Tested | Comments |
|------------------------------------|-------------|--------|----------|
| GetActivePrivateClanFireteamCount  | :x:         | :x:    |          |
| GetAvailableClanFireteams          | :x:         | :x:    |          |
| SearchPublicAvailableClanFireteams | :x:         | :x:    |          |
| GetMyClanFireteams                 | :x:         | :x:    |          |
| GetClanFireteam                    | :x:         | :x:    |          |


### Social Endpoints

| Endpoint              | Implemented | Tested | Comments |
|-----------------------|-------------|--------|----------|
| GetFriendList         | :x:         | :x:    |          |
| GetFriendRequestList  | :x:         | :x:    |          |
| IssueFriendRequest    | :x:         | :x:    |          |
| AcceptFriendRequest   | :x:         | :x:    |          |
| DeclineFriendRequest  | :x:         | :x:    |          |
| RemoveFriend          | :x:         | :x:    |          |
| RemoveFriendRequest   | :x:         | :x:    |          |
| GetPlatformFriendList | :x:         | :x:    |          |


### Core Endpoints

| Endpoint               | Implemented | Tested | Comments |
|------------------------|-------------|--------|----------|
| GetAvailableLocales    | :x:         | :x:    |          |
| GetCommonSettings      | :x:         | :x:    |          |
| GetUserSystemOverrides | :x:         | :x:    |          |
| GetGlobalAlerts        | :x:         | :x:    |          |

---

## Notes

- I plan to create a separate package specifically for integrating with the
Destiny manifest, which will utilize this package as a dependency.