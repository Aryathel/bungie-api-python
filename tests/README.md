# Tests

This package contains a test suite to test what little I can programmatically.
Many of the endpoints require OAuth verification, which there is no consistent
way to automate with something like a [GitHub action](/.github/workflows/test_api_endpoints_workflow.yml).

## Test Comprehension

### OAuth Endpoints

| Endpoint        | Local              | Automated | Comments                                |
|-----------------|--------------------|-----------|-----------------------------------------|
| GetAccessToken  | :heavy_check_mark: | :x:       | Cannot automate test due to OAuth flow. |
| GetRefreshToken | :heavy_check_mark: | :x:       | Cannot automate test due to OAuth flow. |

### App Endpoints

| Endpoint               | Local              | Automated          | Comments                                |
|------------------------|--------------------|--------------------|-----------------------------------------|
| GetApplicationApiUsage | :heavy_check_mark: | :x:                | Cannot automate test due to OAuth flow. |
| GetBungieApplications  | :heavy_check_mark: | :heavy_check_mark: |                                         |

### User Endpoints

| Endpoint                              | Manual             | Automated          | Comments                           |
|---------------------------------------|--------------------|--------------------|------------------------------------|
| GetBungieNetUserById                  | :heavy_check_mark: | :heavy_check_mark: |                                    |
| GetSanitizedPlatformDisplayNames      | :heavy_check_mark: | :heavy_check_mark: |                                    |
| GetCredentialTypesForTargetAccount    | :heavy_check_mark: | :x:                | Cannot automate due to OAuth flow. |
| GetAvailableThemes                    | :x:                | :x:                | Not yet implemented.               |
| GetMembershipDataById                 | :x:                | :x:                | Not yet implemented.               |
| GetMembershipDataForCurrentUser       | :x:                | :x:                | Not yet implemented.               |
| GetMembershipFromHardLinkedCredential | :x:                | :x:                | Not yet implemented.               |
| SearchByGlobalNamePrefix              | :x:                | :x:                | Not yet implemented.               |
| SearchByGlobalNamePost                | :x:                | :x:                | Not yet implemented.               |

### Content Endpoints

| Endpoint                  | Manual | Automated | Comments             |
|---------------------------|--------|-----------|----------------------|
| GetContentType            | :x:    | :x:       | Not yet implemented. |
| GetContentById            | :x:    | :x:       | Not yet implemented. |
| GetContentByTagAndType    | :x:    | :x:       | Not yet implemented. |
| SearchContentWithText     | :x:    | :x:       | Not yet implemented. |
| SearchContentByTagAndType | :x:    | :x:       | Not yet implemented. |
| SearchHelpArticles        | :x:    | :x:       | Not yet implemented. |
| RssNewsArticles           | :x:    | :x:       | Not yet implemented. |

### Forum Endpoints

| Endpoint                         | Manual | Automated | Comments             |
|----------------------------------|--------|-----------|----------------------|
| GetTopicsPaged                   | :x:    | :x:       | Not yet implemented. |
| GetCoreTopicsPaged               | :x:    | :x:       | Not yet implemented. |
| GetPostsThreadedPaged            | :x:    | :x:       | Not yet implemented. |
| GetPostsThreadedPagedFromChild   | :x:    | :x:       | Not yet implemented. |
| GetPostAndParent                 | :x:    | :x:       | Not yet implemented. |
| GetPostAndParentAwaitingApproval | :x:    | :x:       | Not yet implemented. |
| GetTopicForContent               | :x:    | :x:       | Not yet implemented. |
| GetForumTagSuggestions           | :x:    | :x:       | Not yet implemented. |
| GetPoll                          | :x:    | :x:       | Not yet implemented. |
| GetRecruitmentThreadSummaries    | :x:    | :x:       | Not yet implemented. |


### GroupV2 Endpoints

| Endpoint                      | Manual | Automated | Comments             |
|-------------------------------|--------|-----------|----------------------|
| GetAvailableAvatars           | :x:    | :x:       | Not yet implemented. |
| GetAvailableThemes            | :x:    | :x:       | Not yet implemented. |
| GetUserClanInviteSetting      | :x:    | :x:       | Not yet implemented. |
| GetRecommendedGroups          | :x:    | :x:       | Not yet implemented. |
| GroupSearch                   | :x:    | :x:       | Not yet implemented. |
| GetGroup                      | :x:    | :x:       | Not yet implemented. |
| GetGroupByName                | :x:    | :x:       | Not yet implemented. |
| GetGroupByNameV2              | :x:    | :x:       | Not yet implemented. |
| GetGroupOptionalConversations | :x:    | :x:       | Not yet implemented. |
| EditGroup                     | :x:    | :x:       | Not yet implemented. |
| EditClanBanner                | :x:    | :x:       | Not yet implemented. |
| EditFounderOptions            | :x:    | :x:       | Not yet implemented. |
| AddOptionalConversation       | :x:    | :x:       | Not yet implemented. |
| EditOptionalConversation      | :x:    | :x:       | Not yet implemented. |
| GetMembersOfGroup             | :x:    | :x:       | Not yet implemented. |
| GetAdminsAndFounderOfGroup    | :x:    | :x:       | Not yet implemented. |
| EditGroupMembership           | :x:    | :x:       | Not yet implemented. |
| KickMember                    | :x:    | :x:       | Not yet implemented. |
| BanMember                     | :x:    | :x:       | Not yet implemented. |
| UnbanMember                   | :x:    | :x:       | Not yet implemented. |
| GetBannedMembersOfGroup       | :x:    | :x:       | Not yet implemented. |
| AbdicateFoundership           | :x:    | :x:       | Not yet implemented. |
| GetPendingMemberships         | :x:    | :x:       | Not yet implemented. |
| GetInvitedIndividuals         | :x:    | :x:       | Not yet implemented. |
| ApproveAllPending             | :x:    | :x:       | Not yet implemented. |
| DenyAllPending                | :x:    | :x:       | Not yet implemented. |
| ApprovePendingForList         | :x:    | :x:       | Not yet implemented. |
| ApprovePending                | :x:    | :x:       | Not yet implemented. |
| DenyPendingForList            | :x:    | :x:       | Not yet implemented. |
| GetGroupsForMember            | :x:    | :x:       | Not yet implemented. |
| RecoverGroupForFounder        | :x:    | :x:       | Not yet implemented. |
| GetPotentialGroupsForMember   | :x:    | :x:       | Not yet implemented. |
| IndividualGroupInvite         | :x:    | :x:       | Not yet implemented. |
| IndividualGroupInviteCancel   | :x:    | :x:       | Not yet implemented. |


### Tokens Endpoints

| Endpoint                              | Manual | Automated | Comments             |
|---------------------------------------|--------|-----------|----------------------|
| ForceDropsRepair                      | :x:    | :x:       | Not yet implemented. |
| ClaimPartnerOffer                     | :x:    | :x:       | Not yet implemented. |
| ApplyMissingPartnerOffersWithoutClaim | :x:    | :x:       | Not yet implemented. |
| GetPartnerOfferSkuHistory             | :x:    | :x:       | Not yet implemented. |
| GetPartnerRewardHistory               | :x:    | :x:       | Not yet implemented. |
| GetBungieRewardsForUser               | :x:    | :x:       | Not yet implemented. |
| GetBungieRewardsForPlatformUser       | :x:    | :x:       | Not yet implemented. |
| GetBungieRewardsList                  | :x:    | :x:       | Not yet implemented. |


### Destiny2 Endpoints

| Endpoint                                   | Manual | Automated | Comments             |
|--------------------------------------------|--------|-----------|----------------------|
| GetDestinyManifest                         | :x:    | :x:       | Not yet implemented. |
| GetDestinyEntityDefinition                 | :x:    | :x:       | Not yet implemented. |
| SearchDestinyPlayerByBungieName            | :x:    | :x:       | Not yet implemented. |
| GetLinkedProfiles                          | :x:    | :x:       | Not yet implemented. |
| GetProfile                                 | :x:    | :x:       | Not yet implemented. |
| GetCharacter                               | :x:    | :x:       | Not yet implemented. |
| GetClanWeeklyRewardState                   | :x:    | :x:       | Not yet implemented. |
| GetClanBannerSource                        | :x:    | :x:       | Not yet implemented. |
| GetItem                                    | :x:    | :x:       | Not yet implemented. |
| GetVendors                                 | :x:    | :x:       | Not yet implemented. |
| GetVendor                                  | :x:    | :x:       | Not yet implemented. |
| GetPublicVendors                           | :x:    | :x:       | Not yet implemented. |
| GetCollectibleNodeDetails                  | :x:    | :x:       | Not yet implemented. |
| TransferItem                               | :x:    | :x:       | Not yet implemented. |
| PullFromPostmaster                         | :x:    | :x:       | Not yet implemented. |
| EquipItem                                  | :x:    | :x:       | Not yet implemented. |
| EquipItems                                 | :x:    | :x:       | Not yet implemented. |
| SetItemLockState                           | :x:    | :x:       | Not yet implemented. |
| SetQuestTrackedState                       | :x:    | :x:       | Not yet implemented. |
| InsertSocketPlug                           | :x:    | :x:       | Not yet implemented. |
| InsertSocketPlugFree                       | :x:    | :x:       | Not yet implemented. |
| GetPostGameCarnageReport                   | :x:    | :x:       | Not yet implemented. |
| ReportOffensivePostGameCarnageReportPlayer | :x:    | :x:       | Not yet implemented. |
| GetHistoricalStatsDefinition               | :x:    | :x:       | Not yet implemented. |
| GetClanLeaderboards                        | :x:    | :x:       | Not yet implemented. |
| GetClanAggregateStats                      | :x:    | :x:       | Not yet implemented. |
| GetLeaderboards                            | :x:    | :x:       | Not yet implemented. |
| GetLeaderboardsForCharacter                | :x:    | :x:       | Not yet implemented. |
| SearchDestinyEntities                      | :x:    | :x:       | Not yet implemented. |
| GetHistoricalStats                         | :x:    | :x:       | Not yet implemented. |
| GetHistoricalStatsForAccount               | :x:    | :x:       | Not yet implemented. |
| GetActivityHistory                         | :x:    | :x:       | Not yet implemented. |
| GetUniqueWeaponHistory                     | :x:    | :x:       | Not yet implemented. |
| GetDestinyAggregateActivityStats           | :x:    | :x:       | Not yet implemented. |
| GetPublicMilestoneContent                  | :x:    | :x:       | Not yet implemented. |
| GetPublicMilestones                        | :x:    | :x:       | Not yet implemented. |
| AwaInitializeRequest                       | :x:    | :x:       | Not yet implemented. |
| AwaProvideAuthorizationResult              | :x:    | :x:       | Not yet implemented. |
| AwaGetActionToken                          | :x:    | :x:       | Not yet implemented. |


### CommunityContent Endpoint

| Endpoint            | Manual | Automated | Comments             |
|---------------------|--------|-----------|----------------------|
| GetCommunityContent | :x:    | :x:       | Not yet implemented. |


### Trending Endpoints

| Endpoint               | Manual | Automated | Comments             |
|------------------------|--------|-----------|----------------------|
| GetTrendingCategories  | :x:    | :x:       | Not yet implemented. |
| GetTrendingCategory    | :x:    | :x:       | Not yet implemented. |
| GetTrendingEntryDetail | :x:    | :x:       | Not yet implemented. |


### Fireteam Endpoints

| Endpoint                           | Manual | Automated | Comments             |
|------------------------------------|--------|-----------|----------------------|
| GetActivePrivateClanFireteamCount  | :x:    | :x:       | Not yet implemented. |
| GetAvailableClanFireteams          | :x:    | :x:       | Not yet implemented. |
| SearchPublicAvailableClanFireteams | :x:    | :x:       | Not yet implemented. |
| GetMyClanFireteams                 | :x:    | :x:       | Not yet implemented. |
| GetClanFireteam                    | :x:    | :x:       | Not yet implemented. |


### Social Endpoints

| Endpoint              | Manual | Automated | Comments             |
|-----------------------|--------|-----------|----------------------|
| GetFriendList         | :x:    | :x:       | Not yet implemented. |
| GetFriendRequestList  | :x:    | :x:       | Not yet implemented. |
| IssueFriendRequest    | :x:    | :x:       | Not yet implemented. |
| AcceptFriendRequest   | :x:    | :x:       | Not yet implemented. |
| DeclineFriendRequest  | :x:    | :x:       | Not yet implemented. |
| RemoveFriend          | :x:    | :x:       | Not yet implemented. |
| RemoveFriendRequest   | :x:    | :x:       | Not yet implemented. |
| GetPlatformFriendList | :x:    | :x:       | Not yet implemented. |


### Core Endpoints

| Endpoint               | Manual | Automated | Comments             |
|------------------------|--------|-----------|----------------------|
| GetAvailableLocales    | :x:    | :x:       | Not yet implemented. |
| GetCommonSettings      | :x:    | :x:       | Not yet implemented. |
| GetUserSystemOverrides | :x:    | :x:       | Not yet implemented. |
| GetGlobalAlerts        | :x:    | :x:       | Not yet implemented. |
