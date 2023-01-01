# Bungie API Python Wrapper

This is a work in progress python wrapper for the Bungie API.

[MIT License](LICENSE.md)

[Test Information](tests/README.md)

---

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Aryathel/bungie-api-python/test_api_endpoints_workflow.yml)

---

## Planned Features

- :x: Complete API coverage.
  - :heavy_check_mark: OAuth workflow
    - :heavy_check_mark: Token endpoints (access token, refresh token)
    - :heavy_check_mark: OAuth context for endpoints requiring it.
  - :x: Endpoints
    - :heavy_check_mark: App
    - :heavy_check_mark: User
    - :x: Content
    - :x: Forum
    - :x: GroupV2
    - :x: Tokens
    - :x: Destiny2
    - :x: CommunityContent
    - :x: Trending
    - :x: Fireteam
    - :x: Social
    - :x: Common
  - :x: Entity Models
- :heavy_check_mark: Async and sync client implementations.

## Quikstart

A simple synchronous usage example:

```python
import bungie_api_python
from bungie_api_python.entities.core import OAuthClientType

# Anything beyond the api key is optional,
# and only required for endpoints that use OAuth
client = bungie_api_python.BungieClientSync(
  api_key='your_key',
  client_id=000,
  client_secret='client_secret',
  client_type=OAuthClientType.Confidential
)

# Non OAuth endpoints will work right away
apps = client.app.get_bungie_applications()
for app in apps.Response:
  print(f'{app.name}: {app.status}')
# >>> www.bungie.net: ApplicationStatus.Private
# >>> Destiny 2 Companion (Android): ApplicationStatus.Private
# etc...

# If using OAuth, passing in an authorization code will perform the token
# exchange process, and refresh the token as necessary.
client.gen_oauth_context(code='your auth code')

user = client.user.get_membership_data_for_current_user()
print(user.Response.bungieNetUser.uniqueName)
# >>> "Aryathel#7877"
```

The same process can be used for an asynchronous client.
Simply create a `BungieClientAsync` instance rather than a `BungeClientSync`
instance, then `await` your calls (`await client.gen_oauth_context`, `await client.user.get_bungie_applications`, etc.).

## Endpoints

All endpoints `methods` are accessed via the respective client.

`client = BungieClientSync()` then `client.<method>`
`client.oauth.get_access_token`

### OAuth Endpoints

| Endpoint        | Method                     | Implemented        | Tested             | Comments |
|-----------------|----------------------------|--------------------|--------------------|----------|
| GetAccessToken  | oauth.get_access_token     | :heavy_check_mark: | :heavy_check_mark: |          |
| GetRefreshToken | oauth.refresh_access_token | :heavy_check_mark: | :heavy_check_mark: |          |

### App Endpoints

| Endpoint               | Method                        | Implemented        | Tested             | Comments |
|------------------------|-------------------------------|--------------------|--------------------|----------|
| GetApplicationApiUsage | app.get_application_api_usage | :heavy_check_mark: | :heavy_check_mark: |          |
| GetBungieApplications  | app.get_bungie_applications   | :heavy_check_mark: | :heavy_check_mark: |          |

### User Endpoints

| Endpoint                              | Method                                          | Implemented        | Tested             | Comments                                                                                               |
|---------------------------------------|-------------------------------------------------|--------------------|--------------------|--------------------------------------------------------------------------------------------------------|
| GetBungieNetUserById                  | user.get_bungie_net_user_by_id                  | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |
| GetSanitizedPlatformDisplayNames      | user.get_sanitized_platform_display_name        | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |
| GetCredentialTypesForTargetAccount    | user.get_credential_types_for_target_account    | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |
| GetAvailableThemes                    | user.get_available_themes                       | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |
| GetMembershipDataById                 | user.get_membership_data_by_id                  | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |
| GetMembershipDataForCurrentUser       | user.get_membership_data_for_current_user       | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |
| GetMembershipFromHardLinkedCredential | user.get_membership_from_hard_linked_credential | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |
| SearchByGlobalNamePrefix              | user.search_by_global_name_prefix               | :x:                | :x:                | This endpoint is obsolete and will raise an error if called, it is only included for posterity's sake. |
| SearchByGlobalNamePost                | user.search_by_global_name_post                 | :heavy_check_mark: | :heavy_check_mark: |                                                                                                        |

### Content Endpoints

| Endpoint                  | Method | Implemented | Tested  | Comments |
|---------------------------|--------|-------------|---------|----------|
| GetContentType            |        | :x:         | :x:     |          |
| GetContentById            |        | :x:         | :x:     |          |
| GetContentByTagAndType    |        | :x:         | :x:     |          |
| SearchContentWithText     |        | :x:         | :x:     |          |
| SearchContentByTagAndType |        | :x:         | :x:     |          |
| SearchHelpArticles        |        | :x:         | :x:     |          |
| RssNewsArticles           |        | :x:         | :x:     |          |

### Forum Endpoints

| Endpoint                         | Method | Implemented | Tested | Comments |
|----------------------------------|--------|-------------|--------|----------|
| GetTopicsPaged                   |        | :x:         | :x:    |          |
| GetCoreTopicsPaged               |        | :x:         | :x:    |          |
| GetPostsThreadedPaged            |        | :x:         | :x:    |          |
| GetPostsThreadedPagedFromChild   |        | :x:         | :x:    |          |
| GetPostAndParent                 |        | :x:         | :x:    |          |
| GetPostAndParentAwaitingApproval |        | :x:         | :x:    |          |
| GetTopicForContent               |        | :x:         | :x:    |          |
| GetForumTagSuggestions           |        | :x:         | :x:    |          |
| GetPoll                          |        | :x:         | :x:    |          |
| GetRecruitmentThreadSummaries    |        | :x:         | :x:    |          |


### GroupV2 Endpoints

| Endpoint                      | Method | Implemented | Tested | Comments |
|-------------------------------|--------|-------------|--------|----------|
| GetAvailableAvatars           |        | :x:         | :x:    |          |
| GetAvailableThemes            |        | :x:         | :x:    |          |
| GetUserClanInviteSetting      |        | :x:         | :x:    |          |
| GetRecommendedGroups          |        | :x:         | :x:    |          |
| GroupSearch                   |        | :x:         | :x:    |          |
| GetGroup                      |        | :x:         | :x:    |          |
| GetGroupByName                |        | :x:         | :x:    |          |
| GetGroupByNameV2              |        | :x:         | :x:    |          |
| GetGroupOptionalConversations |        | :x:         | :x:    |          |
| EditGroup                     |        | :x:         | :x:    |          |
| EditClanBanner                |        | :x:         | :x:    |          |
| EditFounderOptions            |        | :x:         | :x:    |          |
| AddOptionalConversation       |        | :x:         | :x:    |          |
| EditOptionalConversation      |        | :x:         | :x:    |          |
| GetMembersOfGroup             |        | :x:         | :x:    |          |
| GetAdminsAndFounderOfGroup    |        | :x:         | :x:    |          |
| EditGroupMembership           |        | :x:         | :x:    |          |
| KickMember                    |        | :x:         | :x:    |          |
| BanMember                     |        | :x:         | :x:    |          |
| UnbanMember                   |        | :x:         | :x:    |          |
| GetBannedMembersOfGroup       |        | :x:         | :x:    |          |
| AbdicateFoundership           |        | :x:         | :x:    |          |
| GetPendingMemberships         |        | :x:         | :x:    |          |
| GetInvitedIndividuals         |        | :x:         | :x:    |          |
| ApproveAllPending             |        | :x:         | :x:    |          |
| DenyAllPending                |        | :x:         | :x:    |          |
| ApprovePendingForList         |        | :x:         | :x:    |          |
| ApprovePending                |        | :x:         | :x:    |          |
| DenyPendingForList            |        | :x:         | :x:    |          |
| GetGroupsForMember            |        | :x:         | :x:    |          |
| RecoverGroupForFounder        |        | :x:         | :x:    |          |
| GetPotentialGroupsForMember   |        | :x:         | :x:    |          |
| IndividualGroupInvite         |        | :x:         | :x:    |          |
| IndividualGroupInviteCancel   |        | :x:         | :x:    |          |


### Tokens Endpoints

| Endpoint                              | Method | Implemented | Tested | Comments |
|---------------------------------------|--------|-------------|--------|----------|
| ForceDropsRepair                      |        | :x:         | :x:    |          |
| ClaimPartnerOffer                     |        | :x:         | :x:    |          |
| ApplyMissingPartnerOffersWithoutClaim |        | :x:         | :x:    |          |
| GetPartnerOfferSkuHistory             |        | :x:         | :x:    |          |
| GetPartnerRewardHistory               |        | :x:         | :x:    |          |
| GetBungieRewardsForUser               |        | :x:         | :x:    |          |
| GetBungieRewardsForPlatformUser       |        | :x:         | :x:    |          |
| GetBungieRewardsList                  |        | :x:         | :x:    |          |


### Destiny2 Endpoints

| Endpoint                                   | Method | Implemented | Tested | Comments |
|--------------------------------------------|--------|-------------|--------|----------|
| GetDestinyManifest                         |        | :x:         | :x:    |          |
| GetDestinyEntityDefinition                 |        | :x:         | :x:    |          |
| SearchDestinyPlayerByBungieName            |        | :x:         | :x:    |          |
| GetLinkedProfiles                          |        | :x:         | :x:    |          |
| GetProfile                                 |        | :x:         | :x:    |          |
| GetCharacter                               |        | :x:         | :x:    |          |
| GetClanWeeklyRewardState                   |        | :x:         | :x:    |          |
| GetClanBannerSource                        |        | :x:         | :x:    |          |
| GetItem                                    |        | :x:         | :x:    |          |
| GetVendors                                 |        | :x:         | :x:    |          |
| GetVendor                                  |        | :x:         | :x:    |          |
| GetPublicVendors                           |        | :x:         | :x:    |          |
| GetCollectibleNodeDetails                  |        | :x:         | :x:    |          |
| TransferItem                               |        | :x:         | :x:    |          |
| PullFromPostmaster                         |        | :x:         | :x:    |          |
| EquipItem                                  |        | :x:         | :x:    |          |
| EquipItems                                 |        | :x:         | :x:    |          |
| SetItemLockState                           |        | :x:         | :x:    |          |
| SetQuestTrackedState                       |        | :x:         | :x:    |          |
| InsertSocketPlug                           |        | :x:         | :x:    |          |
| InsertSocketPlugFree                       |        | :x:         | :x:    |          |
| GetPostGameCarnageReport                   |        | :x:         | :x:    |          |
| ReportOffensivePostGameCarnageReportPlayer |        | :x:         | :x:    |          |
| GetHistoricalStatsDefinition               |        | :x:         | :x:    |          |
| GetClanLeaderboards                        |        | :x:         | :x:    |          |
| GetClanAggregateStats                      |        | :x:         | :x:    |          |
| GetLeaderboards                            |        | :x:         | :x:    |          |
| GetLeaderboardsForCharacter                |        | :x:         | :x:    |          |
| SearchDestinyEntities                      |        | :x:         | :x:    |          |
| GetHistoricalStats                         |        | :x:         | :x:    |          |
| GetHistoricalStatsForAccount               |        | :x:         | :x:    |          |
| GetActivityHistory                         |        | :x:         | :x:    |          |
| GetUniqueWeaponHistory                     |        | :x:         | :x:    |          |
| GetDestinyAggregateActivityStats           |        | :x:         | :x:    |          |
| GetPublicMilestoneContent                  |        | :x:         | :x:    |          |
| GetPublicMilestones                        |        | :x:         | :x:    |          |
| AwaInitializeRequest                       |        | :x:         | :x:    |          |
| AwaProvideAuthorizationResult              |        | :x:         | :x:    |          |
| AwaGetActionToken                          |        | :x:         | :x:    |          |


### CommunityContent Endpoint

| Endpoint            | Method | Implemented | Tested | Comments |
|---------------------|--------|-------------|--------|----------|
| GetCommunityContent |        | :x:         | :x:    |          |


### Trending Endpoints

| Endpoint               | Method | Implemented | Tested | Comments |
|------------------------|--------|-------------|--------|----------|
| GetTrendingCategories  |        | :x:         | :x:    |          |
| GetTrendingCategory    |        | :x:         | :x:    |          |
| GetTrendingEntryDetail |        | :x:         | :x:    |          |


### Fireteam Endpoints

| Endpoint                           | Method | Implemented | Tested | Comments |
|------------------------------------|--------|-------------|--------|----------|
| GetActivePrivateClanFireteamCount  |        | :x:         | :x:    |          |
| GetAvailableClanFireteams          |        | :x:         | :x:    |          |
| SearchPublicAvailableClanFireteams |        | :x:         | :x:    |          |
| GetMyClanFireteams                 |        | :x:         | :x:    |          |
| GetClanFireteam                    |        | :x:         | :x:    |          |


### Social Endpoints

| Endpoint              | Method | Implemented | Tested | Comments |
|-----------------------|--------|-------------|--------|----------|
| GetFriendList         |        | :x:         | :x:    |          |
| GetFriendRequestList  |        | :x:         | :x:    |          |
| IssueFriendRequest    |        | :x:         | :x:    |          |
| AcceptFriendRequest   |        | :x:         | :x:    |          |
| DeclineFriendRequest  |        | :x:         | :x:    |          |
| RemoveFriend          |        | :x:         | :x:    |          |
| RemoveFriendRequest   |        | :x:         | :x:    |          |
| GetPlatformFriendList |        | :x:         | :x:    |          |


### Core Endpoints

| Endpoint               | Method | Implemented | Tested | Comments |
|------------------------|--------|-------------|--------|----------|
| GetAvailableLocales    |        | :x:         | :x:    |          |
| GetCommonSettings      |        | :x:         | :x:    |          |
| GetUserSystemOverrides |        | :x:         | :x:    |          |
| GetGlobalAlerts        |        | :x:         | :x:    |          |

---

## Notes

- I plan to create a separate package specifically for integrating with the
Destiny manifest, which will utilize this package as a dependency.