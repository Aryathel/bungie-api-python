import unittest

from generated.entities import ForumTopicsQuickDateEnum, ForumTopicsSortEnum, ForumTopicsCategoryFiltersEnum, \
    ForumPostSortEnum, GroupType, BungieMembershipType, GroupsForMemberFilter, DestinyComponentType, \
    DestinyVendorFilter, DestinyActivityModeType, CommunityContentSortMode, TrendingEntryType, PlatformFriendType, \
    PlatformErrorCodes
from tests.core import TestCore


class TestApp(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [ ] App.GetApplicationApiUsage: Requires OAuth
    - [x] App.GetApplicationApiUsage
    """
    tests = ['test_get_bungie_applications']

    async def test_get_bungie_applications(self) -> None:
        sync_r = self.sync_client.app.get_bungie_applications()
        async_r = await self.async_client.app.get_bungie_applications()
        assert sync_r == async_r
        print('GetBungieApplications: OK')


class TestUser(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [x] User.GetBungieNetUserById
    - [x] User.GetSanitizedPlatformDisplayNames
    - [ ] User.GetCredentialTypesForTargetAccount: Requires OAuth
    - [x] User.GetAvailableThemes
    - [x] User.GetMembershipDataById
    - [ ] User.GetMembershipDataForCurrentUser: Requires OAuth
    - [x] User.GetMembershipFromHardLinkedCredential
    - [x] User.SearchByGlobalNamePrefix
    """
    tests = [
        'test_get_bungie_net_user_by_id',
        'test_get_sanitized_platform_display_names',
        'test_get_available_themes',
        'test_get_membership_data_by_id',
        'test_get_membership_from_hard_linked_credential',
        'test_search_by_global_name_post',
    ]

    async def test_get_bungie_net_user_by_id(self) -> None:
        print(self.sync_client.authorization_url)
        user_id = 19548659
        sync_r = self.sync_client.user.get_bungie_net_user_by_id(user_id)
        async_r = await self.async_client.user.get_bungie_net_user_by_id(user_id)
        assert sync_r == async_r
        print('GetBungieNetUserById: OK')

    async def test_get_sanitized_platform_display_names(self) -> None:
        membership_id = 19548659
        sync_r = self.sync_client.user.get_sanitized_platform_display_names(membership_id)
        async_r = await self.async_client.user.get_sanitized_platform_display_names(membership_id)
        assert sync_r == async_r
        print('GetSanitizedPlatformDisplayNames: OK')

    """ Seems to require OAuth? https://github.com/Bungie-net/api/issues/1769
    async def test_get_credential_types_for_target_account(self) -> None:
        membership_id = 19548659
        sync_r = self.sync_client.user.get_credential_types_for_target_account(membership_id)
        async_r = await self.async_client.user.get_credential_types_for_target_account(membership_id)
        assert sync_r == async_r
        print(sync_r)
    """

    async def test_get_available_themes(self) -> None:
        sync_r = self.sync_client.user.get_available_themes()
        async_r = await self.async_client.user.get_available_themes()
        assert sync_r == async_r
        print('GetAvailableThemes: OK')

    async def test_get_membership_data_by_id(self) -> None:
        membership_id = 19548659
        membership_type = 3
        sync_r = self.sync_client.user.get_membership_data_by_id(
            membership_id=membership_id,
            membership_type=membership_type,
        )
        async_r = await self.async_client.user.get_membership_data_by_id(
            membership_id=membership_id,
            membership_type=membership_type,
        )
        assert sync_r == async_r
        print('GetMembershipDataById: OK')

    async def test_get_membership_from_hard_linked_credential(self) -> None:
        credential = '76561198119241330'
        cr_type = 12
        sync_r = self.sync_client.user.get_membership_from_hard_linked_credential(credential, cr_type)
        async_r = await self.async_client.user.get_membership_from_hard_linked_credential(credential, cr_type)
        assert sync_r == async_r
        print('GetMembershipFromHardLinkedCredential: OK')

    async def test_search_by_global_name_post(self) -> None:
        page = 0
        display_name_prefix = 'Aryathel'
        sync_r = self.sync_client.user.search_by_global_name_post(display_name_prefix=display_name_prefix, page=page)
        async_r = await self.async_client.user.search_by_global_name_post(
            display_name_prefix=display_name_prefix,
            page=page
        )
        assert async_r == sync_r
        print('SearchByGlobalNamePost: OK')


class TestContent(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [x] Content.GetContentType
    - [x] Content.GetContentById
    - [x] Content.GetContentByTagAndType
    - [x] Content.SearchContentWithText
    - [x] Content.SearchContentByTagAndType
    - [x] Content.SearchHelpArticles
    - [x] Content.RssNewsArticles
    """
    tests = [
        'test_get_content_type',
        'test_get_content_by_id',
        'test_get_content_by_tag_and_type',
        'test_search_content_with_text',
        'test_search_content_by_tag_and_type',
        'test_search_help_articles',
        'test_rss_news_articles',
    ]

    async def test_get_content_type(self) -> None:
        c_type = 'news'
        sync_r = self.sync_client.content.get_content_type(c_type)
        async_r = await self.async_client.content.get_content_type(c_type)
        assert sync_r == async_r
        print('GetContentType: OK')

    async def test_get_content_by_id(self) -> None:
        c_id = 51999
        locale = 'en'
        sync_r = self.sync_client.content.get_content_by_id(c_id, locale)
        async_r = await self.async_client.content.get_content_by_id(c_id, locale)
        assert sync_r == async_r
        print('GetContentById: OK')

    async def test_get_content_by_tag_and_type(self) -> None:
        locale = 'en'
        tag = 'twab'
        type = 'news'
        sync_r = self.sync_client.content.get_content_by_tag_and_type(locale, tag, type)
        async_r = await self.async_client.content.get_content_by_tag_and_type(locale, tag, type)
        assert sync_r == async_r
        print('GetContentByTagAndType: OK')

    async def test_search_content_with_text(self) -> None:
        locale = 'en'
        ctype = 'News'
        currentpage = 1
        searchtext = 'Week At Bungie'
        sync_r = self.sync_client.content.search_content_with_text(
            locale=locale,
            ctype=ctype,
            currentpage=currentpage,
            searchtext=searchtext,
        )
        async_r = await self.async_client.content.search_content_with_text(
            locale=locale,
            ctype=ctype,
            currentpage=currentpage,
            searchtext=searchtext,
        )
        assert sync_r == async_r
        print('SearchContentWithText: OK')

    async def test_search_content_by_tag_and_type(self) -> None:
        locale = 'en'
        tag = 'twab'
        ctype = 'News'
        currentpage = 1
        sync_r = self.sync_client.content.search_content_by_tag_and_type(locale, tag, ctype, currentpage)
        async_r = await self.async_client.content.search_content_by_tag_and_type(locale, tag, ctype, currentpage)
        assert sync_r == async_r
        print('SearchContentByTagAndType: OK')

    async def test_search_help_articles(self) -> None:
        searchtext = 'multikill'
        size = 15
        sync_r = self.sync_client.content.search_help_articles(searchtext, size)
        async_r = await self.async_client.content.search_help_articles(searchtext, size)
        assert sync_r == async_r
        print('SearchHelpArticles: OK')

    async def test_rss_news_articles(self) -> None:
        page_token = 0
        category_filter = None
        include_body = False
        sync_r = self.sync_client.content.rss_news_articles(page_token, category_filter, include_body)
        async_r = await self.async_client.content.rss_news_articles(page_token, category_filter, include_body)
        assert sync_r == async_r
        print('RssNewsArticles: OK')


class TestForum(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [x] Forum.GetTopicsPaged
    - [x] Forum.GetCoreTopicsPaged
    - [x] Forum.GetPostsThreadedPaged
    - [x] Forum.GetPostsThreadedPagedFromChild
    - [x] Forum.GetPostAndParent
    - [ ] Forum.GetPostAndParentAwaitingApproval: Scratched due to not having a post awaiting approval to test with.
    - [ ] Forum.GetTopicForContent: Scratched due to not having a content ID to test with.
    - [x] Forum.GetForumTagSuggestions
    - [x] Forum.GetPoll
    - [ ] Forum.GetRecruitmentThreadSummaries: Scratched due to persistent "down for maintenance" error.
    """
    tests = [
        'test_get_topics_paged',
        'test_get_core_topics_paged',
        'test_get_posts_threaded_pages',
        'test_get_posts_threaded_paged_from_child',
        'test_get_post_and_parent',
        # 'test_get_post_and_parent_awaiting_approval',
        # 'test_get_topic_for_content',
        'test_get_forum_tag_suggestions',
        'test_get_poll',
        # 'test_get_recruitment_thread_summaries',
    ]

    async def test_get_topics_paged(self) -> None:
        category_filter = ForumTopicsCategoryFiltersEnum.None_
        group = 2603136
        page = 0
        page_size = 5
        quick_date = ForumTopicsQuickDateEnum.All
        sort = ForumTopicsSortEnum.Default

        sync_r = self.sync_client.forum.get_topics_paged(
            category_filter=category_filter,
            group=group,
            page=page,
            page_size=page_size,
            quick_date=quick_date,
            sort=sort,
            locales='en',
        )
        async_r = await self.async_client.forum.get_topics_paged(
            category_filter=category_filter,
            group=group,
            page=page,
            page_size=page_size,
            quick_date=quick_date,
            sort=sort,
            locales='en',
        )
        assert sync_r == async_r
        print('GetTopicsPaged: OK')

    async def test_get_core_topics_paged(self) -> None:
        page = 0
        sync_r = self.sync_client.forum.get_core_topics_paged(
            category_filter=ForumTopicsCategoryFiltersEnum.TextOnly,
            page=page,
            quick_date=ForumTopicsQuickDateEnum.All,
            sort=ForumTopicsSortEnum.MostUpvoted,
            locales='en'
        )
        async_r = await self.async_client.forum.get_core_topics_paged(
            category_filter=ForumTopicsCategoryFiltersEnum.TextOnly,
            page=page,
            quick_date=ForumTopicsQuickDateEnum.All,
            sort=ForumTopicsSortEnum.MostUpvoted,
            locales='en'
        )
        # Check for just the most upvoted responses matching,
        # because the forums change too quickly to verify the entire response matching.
        assert sync_r.Response.results[0] == async_r.Response.results[0]
        print('GetCoreTopicsPaged: OK')

    async def test_get_posts_threaded_pages(self) -> None:
        get_parent_post = True
        page = 0
        page_size = 5
        parent_post_id = 262235949
        reply_size = 100
        root_thread_mode = True
        sort_mode = ForumPostSortEnum.Default

        sync_r = self.sync_client.forum.get_posts_threaded_paged(
            get_parent_post=get_parent_post,
            page=page,
            page_size=page_size,
            parent_post_id=parent_post_id,
            reply_size=reply_size,
            root_thread_mode=root_thread_mode,
            sort_mode=sort_mode,
        )
        async_r = await self.async_client.forum.get_posts_threaded_paged(
            get_parent_post=get_parent_post,
            page=page,
            page_size=page_size,
            parent_post_id=parent_post_id,
            reply_size=reply_size,
            root_thread_mode=root_thread_mode,
            sort_mode=sort_mode,
        )
        assert sync_r == async_r
        print('GetPostsThreadedPaged: OK')

    async def test_get_posts_threaded_paged_from_child(self) -> None:
        child_post_id = 262235995
        page = 0
        page_size = 100
        reply_size = 100
        root_thread_mode = False
        sort_mode = ForumPostSortEnum.Default
        showbanned = '1'

        sync_r = self.sync_client.forum.get_posts_threaded_paged_from_child(
            child_post_id=child_post_id,
            page=page,
            page_size=page_size,
            reply_size=reply_size,
            root_thread_mode=root_thread_mode,
            sort_mode=sort_mode,
            showbanned=showbanned,
        )
        async_r = await self.async_client.forum.get_posts_threaded_paged_from_child(
            child_post_id=child_post_id,
            page=page,
            page_size=page_size,
            reply_size=reply_size,
            root_thread_mode=root_thread_mode,
            sort_mode=sort_mode,
            showbanned=showbanned,
        )

        assert async_r == sync_r
        print('GetPostsThreadedPagedFromChild: OK')

    async def test_get_post_and_parent(self) -> None:
        child_post_id = 262235995
        showbanned = '1'

        sync_r = self.sync_client.forum.get_post_and_parent(
            child_post_id=child_post_id,
            showbanned=showbanned,
        )
        async_r = await self.async_client.forum.get_post_and_parent(
            child_post_id=child_post_id,
            showbanned=showbanned,
        )
        assert sync_r == async_r
        print('GetPostAndParent: OK')

    """
    async def test_get_post_and_parent_awaiting_approval(self) -> None:
        child_post_id = 262235995
        showbanned = '1'

        sync_r = self.sync_client.forum.get_post_and_parent_awaiting_approval(
            child_post_id=child_post_id,
            showbanned=showbanned,
        )
        async_r = await self.async_client.forum.get_post_and_parent_awaiting_approval(
            child_post_id=child_post_id,
            showbanned=showbanned,
        )
        assert sync_r == async_r
        print('GetPostAndParentAwaitingApproval: OK')
    """

    """
    async def test_get_topic_for_content(self) -> None:
        content_id = 123

        sync_r = self.sync_client.forum.get_topic_for_content(content_id)
        async_r = await self.async_client.forum.get_topic_for_content(content_id)
        assert sync_r == async_r
        print('GetTopicForContent: OK')
    """

    async def test_get_forum_tag_suggestions(self) -> None:
        partial_tag = '#destiny'
        sync_r = self.sync_client.forum.get_forum_tag_suggestions(partial_tag)
        async_r = await self.async_client.forum.get_forum_tag_suggestions(partial_tag)
        assert sync_r == async_r
        print('GetForumTagSuggestions: OK')

    async def test_get_poll(self) -> None:
        topic_id = 262238856
        sync_r = self.sync_client.forum.get_poll(topic_id)
        async_r = await self.async_client.forum.get_poll(topic_id)
        assert sync_r == async_r
        print('GetPoll: OK')

    """
    async def test_get_recruitment_thread_summaries(self) -> None:
        ids = [262240321]
        sync_r = self.sync_client.forum.get_recruitment_thread_summaries(ids)
        async_r = await self.async_client.forum.get_recruitment_thread_summaries(ids)
        assert sync_r == async_r
        print('GetRecruitmentThreadSummaries: OK')
    """


class TestGroupV2(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [x] GroupV2.GetAvailableAvatars
    - [x] GroupV2.GetAvailableThemes
    - [ ] GroupV2.GetUserClanInviteSetting: Requires OAuth
    - [ ] GroupV2.GetRecommendedGroups: Requires OAuth
    - [x] GroupV2.GroupSearch
    - [x] GroupV2.GetGroup
    - [x] GroupV2.GetGroupByName
    - [x] GroupV2.GetGroupByNameV2
    - [x] GroupV2.GetGroupOptionalConversations
    - [ ] GroupV2.EditGroup: Excluded due to not wanting to edit a clan.
    - [ ] GroupV2.EditClanBanner: Excluded due to not wanting to edit a clan.
    - [ ] GroupV2.EditFounderOptions: Excluded due to not wanting to edit a clan.
    - [ ] GroupV2.AddOptionalConversation: Excluded due to not wanting to edit a clan.
    - [ ] GroupV2.EditOptionalConversation: Excluded due to not wanting to edit a clan.
    - [x] GroupV2.GetMembersOfGroup
    - [x] GroupV2.GetAdminsAndFounderOfGroup
    - [ ] GroupV2.EditGroupMembership: Excluded due to not wanting to edit any memberships.
    - [ ] GroupV2.KickMember: Excluded due to not wanting to kick any members.
    - [ ] GroupV2.BanMember: Excluded due to not wanting to ban any members.
    - [ ] GroupV2.UnbanMember: Excluded due to not wanting to unban any members.
    - [ ] GroupV2.GetBannedMembersOfGroup: Excluded due to requiring OAuth.
    - [ ] GroupV2.AbdicateFoundership: Excluded due to not wanting to abdicate foundership.
    - [ ] GroupV2.GetPendingMemberships: Excluded due to requiring OAuth.
    - [ ] GroupV2.GetInvitedIndividuals: Excluded due to requiring OAuth.
    - [ ] GroupV2.ApproveAllPending: Excluded due to not wanting to approve pending memberships.
    - [ ] GroupV2.DenyAllPending: Excluded due to not wanting to deny pending memberships.
    - [ ] GroupV2.ApprovePendingForList: Excluded due to not wanting to approve pending memberships.
    - [ ] GroupV2.ApprovePending: Excluded due to not wanting to approve pending memberships.
    - [ ] GroupV2.DenyPendingForList: Excluded due to not wanting to deny pending memberships.
    - [x] GroupV2.GetGroupsForMember
    - [ ] GroupV2.RecoverGroupForFounder: Excluded due to OAuth requirement.
    - [x] GroupV2.GetPotentialGroupsForMember
    - [ ] GroupV2.IndividualGroupInvite: Excluded due to not wanting to invite members.
    - [ ] GroupV2.IndividualGroupInviteCancel: Excluded due to not wanting to cancel member invites.
    """
    tests = [
        'test_get_available_avatars',
        'test_get_available_themes',
        'test_group_search',
        'test_get_group',
        'test_get_group_by_name',
        'test_get_group_by_name_v2',
        'test_get_group_optional_conversations',
        'test_get_members_of_group',
        'test_get_admins_and_founder_of_group',
        'test_get_groups_for_member',
        # 'test_recover_group_for_founder',
        'test_get_potential_groups_for_member',
    ]

    async def test_get_available_avatars(self) -> None:
        sync_r = self.sync_client.group_v2.get_available_avatars()
        async_r = await self.async_client.group_v2.get_available_avatars()
        assert sync_r == async_r
        print('GetAvailableAvatars: OK')

    async def test_get_available_themes(self) -> None:
        sync_r = self.sync_client.group_v2.get_available_themes()
        async_r = await self.async_client.group_v2.get_available_themes()
        assert sync_r == async_r
        print('GetAvailableThemes: OK')

    async def test_group_search(self) -> None:
        name = 'Slicing Squall'
        gt = GroupType.Clan

        sync_r = self.sync_client.group_v2.group_search(
            name=name,
            group_type=gt,
        )
        async_r = await self.async_client.group_v2.group_search(
            name=name,
            group_type=gt,
        )
        assert sync_r == async_r
        print('GroupSearch: OK')

    async def test_get_group(self) -> None:
        group_id = 2603136
        sync_r = self.sync_client.group_v2.get_group(group_id)
        async_r = await self.async_client.group_v2.get_group(group_id)
        assert sync_r == async_r
        print('GetGroup: OK')

    async def test_get_group_by_name(self) -> None:
        group_name = 'Slicing Squall'
        group_type = GroupType.Clan
        sync_r = self.sync_client.group_v2.get_group_by_name(group_name, group_type)
        async_r = await self.async_client.group_v2.get_group_by_name(group_name, group_type)
        assert sync_r == async_r
        print('GetGroupByName: OK')

    async def test_get_group_by_name_v2(self) -> None:
        group_name = 'Slicing Squall'
        group_type = GroupType.Clan
        sync_r = self.sync_client.group_v2.get_group_by_name_v2(group_name, group_type)
        async_r = await self.async_client.group_v2.get_group_by_name_v2(group_name, group_type)
        assert sync_r == async_r
        print('GetGroupByNameV2: OK')

    async def test_get_group_optional_conversations(self) -> None:
        group_id = 2603136
        sync_r = self.sync_client.group_v2.get_group_optional_conversations(group_id)
        async_r = await self.async_client.group_v2.get_group_optional_conversations(group_id)
        assert async_r == sync_r
        print('GetGroupOptionalConversations: OK')

    async def test_get_members_of_group(self) -> None:
        group_id = 2603136
        current_page = 1
        name_search = 'Ar'
        sync_r = self.sync_client.group_v2.get_members_of_group(
            currentpage=current_page,
            group_id=group_id,
            name_search=name_search,
        )
        async_r = await self.async_client.group_v2.get_members_of_group(
            currentpage=current_page,
            group_id=group_id,
            name_search=name_search,
        )
        assert async_r == sync_r
        print('GetMembersOfGroup: OK')

    async def test_get_admins_and_founder_of_group(self) -> None:
        group_id = 2603136
        current_page = 1
        sync_r = self.sync_client.group_v2.get_admins_and_founder_of_group(current_page, group_id)
        async_r = await self.async_client.group_v2.get_admins_and_founder_of_group(current_page, group_id)
        assert sync_r == async_r
        print('GetAdminsAndFounderOfGroup: OK')

    async def test_get_groups_for_member(self) -> None:
        filter = GroupsForMemberFilter.All
        group_type = GroupType.Clan
        membership_id = 19548659
        membership_type = BungieMembershipType.BungieNext
        sync_r = self.sync_client.group_v2.get_groups_for_member(
            filter=filter,
            group_type=group_type,
            membership_id=membership_id,
            membership_type=membership_type,
        )
        async_r = await self.async_client.group_v2.get_groups_for_member(
            filter=filter,
            group_type=group_type,
            membership_id=membership_id,
            membership_type=membership_type,
        )
        assert sync_r.ErrorCode == async_r.ErrorCode == PlatformErrorCodes.Success
        print('GetGroupsForMember: OK')

    """
    async def test_recover_group_for_founder(self) -> None:
        group_type = GroupType.Clan
        membership_id = 19548659
        membership_type = BungieMembershipType.BungieNext
        sync_r = self.sync_client.group_v2.recover_group_for_founder(
            group_type, membership_id, membership_type
        )
        async_r = await self.async_client.group_v2.recover_group_for_founder(
            group_type, membership_id, membership_type
        )
        assert sync_r == async_r
        print('RecoverGroupForFounder: OK')
    """

    async def test_get_potential_groups_for_member(self) -> None:
        filter = GroupsForMemberFilter.All
        group_type = GroupType.Clan
        membership_id = 19548659
        membership_type = BungieMembershipType.BungieNext
        sync_r = self.sync_client.group_v2.get_potential_groups_for_member(
            filter=filter,
            group_type=group_type,
            membership_id=membership_id,
            membership_type=membership_type,
        )
        async_r = await self.async_client.group_v2.get_potential_groups_for_member(
            filter=filter,
            group_type=group_type,
            membership_id=membership_id,
            membership_type=membership_type,
        )
        assert sync_r == async_r
        print('GetPotentialGroupsForMember: OK')


class TestTokens(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [ ] Tokens.ForceDropsRepair: Excluded due to OAuth requirement.
    - [ ] Tokens.ClaimPartnerOffer: Excluded due to OAuth requirement.
    - [ ] Tokens.ApplyMissingPartnerOffersWithoutClaim: Excluded due to OAuth requirement.
    - [ ] Tokens.GetPartnerOfferSkuHistory: Excluded due to OAuth requirement.
    - [ ] Tokens.GetPartnerRewardHistory: Excluded due to OAuth requirement.
    - [ ] Tokens.GetBungieRewardsForUser: Excluded due to OAuth requirement.
    - [ ] Tokens.GetBungieRewardsForPlatformUser: Excluded due to OAuth requirement.
    - [x] Tokens.GetBungieRewardsList
    """
    tests = [
        'test_get_bungie_reward_list',
    ]

    async def test_get_bungie_reward_list(self) -> None:
        sync_r = self.sync_client.tokens.get_bungie_rewards_list()
        async_r = await self.async_client.tokens.get_bungie_rewards_list()
        assert sync_r == async_r
        print('GetBungieRewardList: OK')


class TestDestiny2(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [x] Destiny2.GetDestinyManifest
    - [x] Destiny2.GetDestinyEntityDefinition
    - [x] Destiny2.SearchDestinyPlayerByBungieName
    - [x] Destiny2.GetLinkedProfiles
    - [x] Destiny2.GetProfile
    - [x] Destiny2.GetCharacter
    - [x] Destiny2.GetClanWeeklyRewardState
    - [x] Destiny2.GetClanBannerSource
    - [x] Destiny2.GetItem
    - [ ] Destiny2.GetVendors: Always get an "InsufficientPrivileges" error, likely needs OAuth.
    - [ ] Destiny2.GetVendor: Always get an "InsufficientPrivileges" error, likely needs OAuth.
    - [x] Destiny2.GetPublicVendors
    - [x] Destiny2.GetCollectibleNodeDetails
    - [ ] Destiny2.TransferItem: Requires OAuth
    - [ ] Destiny2.PullFromPostmaster: Requires OAuth
    - [ ] Destiny2.EquipItem: Requires OAuth
    - [ ] Destiny2.EquipItems: Requires OAuth
    - [ ] Destiny2.SetItemLockState: Requires OAuth
    - [ ] Destiny2.SetQuestTrackedState: Requires OAuth
    - [ ] Destiny2.InsertSocketPlug: Requires OAuth
    - [ ] Destiny2.InsertSocketPlugFree: Requires OAuth
    - [x] Destiny2.GetPostGameCarnageReport
    - [ ] Destiny2.ReportOffensivePostGameCarnageReportPlayer: Requires OAuth
    - [x] Destiny2.GetHistoricalStatsDefinition
    - [x] Destiny2.GetClanLeaderboards
    - [x] Destiny2.GetClanAggregateStats
    - [ ] Destiny2.GetLeaderboards: Excluded because it currently is not yet returning usable data.
    - [ ] Destiny2.GetLeaderboardsForCharacter: Requires OAuth
    - [x] Destiny2.SearchDestinyEntities
    - [x] Destiny2.GetHistoricalStats
    - [x] Destiny2.GetHistoricalStatsForAccount
    - [x] Destiny2.GetActivityHistory
    - [x] Destiny2.GetUniqueWeaponHistory
    - [x] Destiny2.GetDestinyAggregateActivityStats
    - [x] Destiny2.GetPublicMilestoneContent
    - [x] Destiny2.GetPublicMilestones
    - [ ] Destiny2.AwaInitializeRequest: Requires OAuth.
    - [ ] Destiny2.AwaProvideAuthorizationResult: Requires Awa workflow, which requires OAuth.
    - [ ] Destiny2.AwaGetActionToken: Requires OAuth.
    """
    tests = [
        'test_get_destiny_manifest',
        'test_get_destiny_entity_definition',
        'test_search_destiny_player_by_bungie_name',
        'test_get_linked_profiles',
        'test_get_profile',
        'test_get_character',
        'test_get_clan_weekly_reward_state',
        'test_get_clan_banner_source',
        'test_get_item',
        # 'test_get_vendors',
        # 'test_get_vendor',
        'test_get_public_vendors',
        'test_get_collectible_node_details',
        'test_get_post_game_carnage_report',
        'test_get_historical_stats_definition',
        'test_get_clan_leaderboards',
        'test_get_clan_aggregate_stats',
        # 'test_get_leaderboards',
        # 'test_get_leaderboards_for_character',
        'test_search_destiny_entities',
        'test_get_historical_stats',
        'test_get_historical_stats_for_account',
        'test_get_activity_history',
        'test_get_unique_weapon_history',
        'test_get_destiny_aggregate_activity_stats',
        'test_get_public_milestone_content',
        'test_get_public_milestones',
    ]

    async def test_get_destiny_manifest(self) -> None:
        sync_r = self.sync_client.destiny2.get_destiny_manifest()
        async_r = await self.async_client.destiny2.get_destiny_manifest()
        assert sync_r == async_r
        print('GetDestinyManifest: OK')

    async def test_get_destiny_entity_definition(self) -> None:
        entity_type = 'DestinyInventoryItemDefinition'
        hash_id = 3588934839
        sync_r = self.sync_client.destiny2.get_destiny_entity_definition(
            entity_type=entity_type,
            hash_identifier=hash_id,
        )
        async_r = await self.async_client.destiny2.get_destiny_entity_definition(
            entity_type=entity_type,
            hash_identifier=hash_id,
        )
        assert sync_r == async_r
        print('GetDestinyEntityDefinition: OK')

    async def test_search_destiny_player_by_bungie_name(self) -> None:
        membership_type = BungieMembershipType.TigerSteam
        name = 'Aryathel'
        code = 7877
        sync_r = self.sync_client.destiny2.search_destiny_player_by_bungie_name(
            membership_type=membership_type,
            display_name=name,
            display_name_code=code,
        )
        async_r = await self.async_client.destiny2.search_destiny_player_by_bungie_name(
            membership_type=membership_type,
            display_name=name,
            display_name_code=code,
        )
        assert sync_r == async_r
        print('SearchDestinyPlayerByBungieName: OK')

    async def test_get_linked_profiles(self) -> None:
        membership_id = 4611686018483530949
        membership_type = BungieMembershipType.TigerSteam
        sync_r = self.sync_client.destiny2.get_linked_profiles(
            membership_id=membership_id,
            membership_type=membership_type,
        )
        async_r = await self.async_client.destiny2.get_linked_profiles(
            membership_id=membership_id,
            membership_type=membership_type,
        )
        assert sync_r == async_r
        print('GetLinkedProfiles: OK')

    async def test_get_profile(self) -> None:
        membership_id = 4611686018483530949
        membership_type = BungieMembershipType.TigerSteam
        components = [
            DestinyComponentType.VendorReceipts,
            DestinyComponentType.ProfileInventories,
            DestinyComponentType.ProfileCurrencies,
            DestinyComponentType.Profiles,
            DestinyComponentType.PlatformSilver,
            DestinyComponentType.Kiosks,
            DestinyComponentType.ItemSockets,
            DestinyComponentType.ProfileProgression,
            DestinyComponentType.PresentationNodes,
            DestinyComponentType.Records,
            DestinyComponentType.Collectibles,
            DestinyComponentType.Transitory,
            DestinyComponentType.Metrics,
            DestinyComponentType.StringVariables,
            DestinyComponentType.Characters,
            DestinyComponentType.CharacterInventories,
            DestinyComponentType.CharacterProgressions,
            DestinyComponentType.CharacterRenderData,
            DestinyComponentType.CharacterActivities,
            DestinyComponentType.CharacterEquipment,
            DestinyComponentType.Craftables,
            DestinyComponentType.CurrencyLookups,
        ]
        sync_r = self.sync_client.destiny2.get_profile(
            membership_id,
            membership_type,
            components,
        )
        async_r = await self.async_client.destiny2.get_profile(
            membership_id,
            membership_type,
            components,
        )
        # Checking for equivalence on sub fields because timestamps do not align in full object.
        assert sync_r.Response.characterEquipment == async_r.Response.characterEquipment
        print('GetProfile: OK')

    async def test_get_character(self) -> None:
        character_id = 2305843009402927792
        membership_id = 4611686018483530949
        membership_type = BungieMembershipType.TigerSteam
        components = [
            DestinyComponentType.VendorReceipts,
            DestinyComponentType.ProfileInventories,
            DestinyComponentType.ProfileCurrencies,
            DestinyComponentType.Profiles,
            DestinyComponentType.PlatformSilver,
            DestinyComponentType.Kiosks,
            DestinyComponentType.ItemSockets,
            DestinyComponentType.ProfileProgression,
            DestinyComponentType.PresentationNodes,
            DestinyComponentType.Records,
            DestinyComponentType.Collectibles,
            DestinyComponentType.Transitory,
            DestinyComponentType.Metrics,
            DestinyComponentType.StringVariables,
            DestinyComponentType.Characters,
            DestinyComponentType.CharacterInventories,
            DestinyComponentType.CharacterProgressions,
            DestinyComponentType.CharacterRenderData,
            DestinyComponentType.CharacterActivities,
            DestinyComponentType.CharacterEquipment,
            DestinyComponentType.Craftables,
            DestinyComponentType.CurrencyLookups,
        ]
        sync_r = self.sync_client.destiny2.get_character(character_id, membership_id, membership_type, components)
        async_r = await self.async_client.destiny2.get_character(
            character_id, membership_id, membership_type, components
        )

        assert sync_r == async_r
        print('GetCharacter: OK')

    async def test_get_clan_weekly_reward_state(self) -> None:
        group_id = 2603136
        sync_r = self.sync_client.destiny2.get_clan_weekly_reward_state(group_id)
        async_r = await self.async_client.destiny2.get_clan_weekly_reward_state(group_id)
        assert sync_r == async_r
        print('GetClanWeeklyRewardState: OK')

    async def test_get_clan_banner_source(self) -> None:
        sync_r = self.sync_client.destiny2.get_clan_banner_source()
        async_r = await self.async_client.destiny2.get_clan_banner_source()
        assert sync_r == async_r
        print('GetClanBannerSource: OK')

    async def test_get_item(self) -> None:
        membership_type = BungieMembershipType.TigerSteam
        membership_id = 4611686018483530949
        instance_id = 6917529203966197229
        components = [
            DestinyComponentType.ItemCommonData,
            DestinyComponentType.ItemInstances,
            DestinyComponentType.ItemObjectives,
            DestinyComponentType.ItemPerks,
            DestinyComponentType.ItemRenderData,
            DestinyComponentType.ItemStats,
            DestinyComponentType.ItemTalentGrids,
            DestinyComponentType.ItemSockets,
            DestinyComponentType.ItemReusablePlugs,
            DestinyComponentType.ItemPlugObjectives,
        ]

        sync_r = self.sync_client.destiny2.get_item(
            destiny_membership_id=membership_id,
            item_instance_id=instance_id,
            membership_type=membership_type,
            components=components,
        )
        async_r = await self.async_client.destiny2.get_item(
            destiny_membership_id=membership_id,
            item_instance_id=instance_id,
            membership_type=membership_type,
            components=components,
        )
        assert sync_r == async_r
        print('GetItem: OK')

    """
    async def test_get_vendors(self) -> None:
        membership_type = BungieMembershipType.TigerSteam
        membership_id = 4611686018483530949
        character_id = 2305843009402927792
        components = [
            DestinyComponentType.Vendors,
            DestinyComponentType.VendorCategories,
            DestinyComponentType.VendorSales,
            DestinyComponentType.CurrencyLookups,
            DestinyComponentType.StringVariables,
        ]
        filter = DestinyVendorFilter.None_

        sync_r = self.sync_client.destiny2.get_vendors(
            character_id=character_id,
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            components=components,
            filter=filter,
        )
        async_r = await self.async_client.destiny2.get_vendors(
            character_id=character_id,
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            components=components,
            filter=filter,
        )
        assert sync_r == async_r
        print('GetVendors: OK')

    async def test_get_vendor(self) -> None:
        membership_type = BungieMembershipType.TigerSteam
        membership_id = 4611686018483530949
        character_id = 2305843009402927792
        components = [
            DestinyComponentType.Vendors,
            DestinyComponentType.VendorCategories,
            DestinyComponentType.VendorSales,
            DestinyComponentType.CurrencyLookups,
            DestinyComponentType.StringVariables,
        ]
        vendor_hash = 672118013

        sync_r = self.sync_client.destiny2.get_vendor(
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            character_id=character_id,
            components=components,
            vendor_hash=vendor_hash,
        )
        async_r = await self.async_client.destiny2.get_vendor(
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            character_id=character_id,
            components=components,
            vendor_hash=vendor_hash,
        )
        assert sync_r == async_r
        print('GetVendor: OK')
    """

    async def test_get_public_vendors(self) -> None:
        components = [
            DestinyComponentType.Vendors,
            DestinyComponentType.VendorCategories,
            DestinyComponentType.VendorSales,
            DestinyComponentType.StringVariables,
        ]

        sync_r = self.sync_client.destiny2.get_public_vendors(components)
        async_r = await self.async_client.destiny2.get_public_vendors(components)
        assert sync_r.Response.vendors == async_r.Response.vendors
        print('GetPublicVendors: OK')

    async def test_get_collectible_node_details(self) -> None:
        membership_type = BungieMembershipType.TigerSteam
        membership_id = 4611686018483530949
        character_id = 2305843009402927792
        presentation_node_hash = 2174985928
        components = [DestinyComponentType.Collectibles]

        sync_r = self.sync_client.destiny2.get_collectible_node_details(
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            character_id=character_id,
            collectible_presentation_node_hash=presentation_node_hash,
            components=components,
        )
        async_r = await self.async_client.destiny2.get_collectible_node_details(
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            character_id=character_id,
            collectible_presentation_node_hash=presentation_node_hash,
            components=components,
        )
        assert sync_r == async_r
        print('GetCollectibleNodeDetails: OK')

    async def test_get_post_game_carnage_report(self) -> None:
        activity_id = 12272982816

        sync_r = self.sync_client.destiny2.get_post_game_carnage_report(activity_id)
        async_r = await self.async_client.destiny2.get_post_game_carnage_report(activity_id)

        assert sync_r == async_r
        print('GetPostGameCarnageReport: OK')

    async def test_get_historical_stats_definition(self) -> None:
        sync_r = self.sync_client.destiny2.get_historical_stats_definition()
        async_r = await self.async_client.destiny2.get_historical_stats_definition()
        assert sync_r == async_r
        print('TestGetHistoricalStatsDefinition: OK')

    async def test_get_clan_leaderboards(self) -> None:
        group_id = 2603136
        max_top = 10
        modes = DestinyActivityModeType.Raid
        stat_id = None

        sync_r = self.sync_client.destiny2.get_clan_leaderboards(
            group_id=group_id,
            maxtop=max_top,
            modes=modes.name,
            statid=stat_id,
        )
        async_r = await self.async_client.destiny2.get_clan_leaderboards(
            group_id=group_id,
            maxtop=max_top,
            modes=modes.name,
            statid=stat_id,
        )
        assert sync_r == async_r
        print('GetClanLeaderboards: OK')

    async def test_get_clan_aggregate_stats(self) -> None:
        group_id = 2603136
        modes = DestinyActivityModeType.Raid

        sync_r = self.sync_client.destiny2.get_clan_aggregate_stats(group_id=group_id, modes=modes.name)
        async_r = await self.async_client.destiny2.get_clan_aggregate_stats(group_id=group_id, modes=modes.name)
        assert sync_r == async_r
        print('GetClanAggregateStats: OK')

    """
    async def test_get_leaderboards(self) -> None:
        membership_type = BungieMembershipType.TigerSteam
        membership_id = 4611686018483530949
        max_top = 10
        modes = DestinyActivityModeType.Raid
        stat_id = None

        sync_r = self.sync_client.destiny2.get_leaderboards(
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            maxtop=max_top,
            modes=modes.name,
            statid=stat_id,
        )
        async_r = await self.async_client.destiny2.get_leaderboards(
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            maxtop=max_top,
            modes=modes.name,
            statid=stat_id,
        )
        assert async_r == sync_r
        print('GetLeaderboards: OK')
    """

    """
    async def test_get_leaderboards_for_character(self) -> None:
        character_id = 2305843009402927792
        membership_id = 4611686018483530949
        membership_type = BungieMembershipType.TigerSteam
        max_top = 10
        modes = DestinyActivityModeType.Raid
        stat_id = None

        sync_r = self.sync_client.destiny2.get_leaderboards_for_character(
            character_id=character_id,
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            maxtop=max_top,
            modes=modes.name,
            statid=stat_id,
        )
        async_r = await self.async_client.destiny2.get_leaderboards_for_character(
            character_id=character_id,
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            maxtop=max_top,
            modes=modes.name,
            statid=stat_id,
        )

        assert sync_r == async_r
        print('GetLeaderboardsForCharacter: OK')
    """

    async def test_search_destiny_entities(self) -> None:
        s_type = 'DestinyInventoryItemDefinition'
        term = 'le monarque'
        page = 0

        sync_r = self.sync_client.destiny2.search_destiny_entities(
            search_term=term,
            type=s_type,
            page=page,
        )
        async_r = await self.async_client.destiny2.search_destiny_entities(
            search_term=term,
            type=s_type,
            page=page,
        )
        assert sync_r == async_r
        print('SearchDestinyEntities: OK')

    async def test_get_historical_stats(self) -> None:
        membership_type = BungieMembershipType.TigerSteam
        membership_id = 4611686018483530949
        character_id = 2305843009402927792

        sync_r = self.sync_client.destiny2.get_historical_stats(
            membership_type=membership_type,
            destiny_membership_id=membership_id,
            character_id=character_id,
        )
        async_r = await self.async_client.destiny2.get_historical_stats(
            membership_type=membership_type,
            destiny_membership_id=membership_id,
            character_id=character_id,
        )
        assert sync_r == async_r
        print('GetHistoricalStats: OK')

    async def test_get_historical_stats_for_account(self) -> None:
        membership_type = BungieMembershipType.TigerSteam
        membership_id = 4611686018483530949

        sync_r = self.sync_client.destiny2.get_historical_stats_for_account(
            destiny_membership_id=membership_id,
            membership_type=membership_type,
        )
        async_r = await self.async_client.destiny2.get_historical_stats_for_account(
            destiny_membership_id=membership_id,
            membership_type=membership_type,
        )
        assert async_r == sync_r
        print('GetHistoricalStatsForAccount: OK')

    async def test_get_activity_history(self) -> None:
        membership_type = BungieMembershipType.TigerSteam
        membership_id = 4611686018483530949
        character_id = 2305843009402927792
        count = 5
        mode = DestinyActivityModeType.Raid
        page = 0

        sync_r = self.sync_client.destiny2.get_activity_history(
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            character_id=character_id,
            count=count,
            mode=mode,
            page=page,
        )
        async_r = await self.async_client.destiny2.get_activity_history(
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            character_id=character_id,
            count=count,
            mode=mode,
            page=page,
        )
        assert sync_r == async_r
        print('GetActivityHistory: OK')

    async def test_get_unique_weapon_history(self) -> None:
        membership_type = BungieMembershipType.TigerSteam
        membership_id = 4611686018483530949
        character_id = 2305843009402927792

        sync_r = self.sync_client.destiny2.get_unique_weapon_history(
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            character_id=character_id,
        )
        async_r = await self.async_client.destiny2.get_unique_weapon_history(
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            character_id=character_id,
        )
        assert sync_r == async_r
        print('GetUniqueWeaponHistory: OK')

    async def test_get_destiny_aggregate_activity_stats(self) -> None:
        membership_type = BungieMembershipType.TigerSteam
        membership_id = 4611686018483530949
        character_id = 2305843009402927792

        sync_r = self.sync_client.destiny2.get_destiny_aggregate_activity_stats(
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            character_id=character_id,
        )
        async_r = await self.async_client.destiny2.get_destiny_aggregate_activity_stats(
            destiny_membership_id=membership_id,
            membership_type=membership_type,
            character_id=character_id,
        )
        assert sync_r == async_r
        print('GetDestinyAggregateActivityStats: OK')

    async def test_get_public_milestone_content(self) -> None:
        milestone_hash = 4253138191

        sync_r = self.sync_client.destiny2.get_public_milestone_content(milestone_hash)
        async_r = await self.async_client.destiny2.get_public_milestone_content(milestone_hash)

        assert sync_r == async_r
        print('GetPublicMilestoneContent: OK')

    async def test_get_public_milestones(self) -> None:
        sync_r = self.sync_client.destiny2.get_public_milestones()
        async_r = await self.async_client.destiny2.get_public_milestones()

        assert sync_r == async_r
        print('GetPublicMilestones: OK')


class TestCommunityContent(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [x] CommunityContent.GetCommunityContent
    """
    tests = [
        'test_get_community_content',
    ]

    async def test_get_community_content(self) -> None:
        sort = ForumTopicsCategoryFiltersEnum.None_
        page = 0
        media_filter = CommunityContentSortMode.Latest

        sync_r = self.sync_client.community_content.get_community_content(
            media_filter=media_filter,
            page=page,
            sort=sort,
        )
        async_r = await self.async_client.community_content.get_community_content(
            media_filter=media_filter,
            page=page,
            sort=sort,
        )
        assert sync_r == async_r
        print('GetCommunityContent: OK')


class TestTrending(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [x] Trending.GetTrendingCategories
    - [x] Trending.GetTrendingCategory
    - [x] Trending.GetTrendingEntryDetail
    """
    tests = [
        'test_get_trending_categories',
        'test_get_trending_category',
        'test_get_trending_entry_detail',
    ]

    async def test_get_trending_categories(self) -> None:
        sync_r = self.sync_client.trending.get_trending_categories()
        async_r = await self.async_client.trending.get_trending_categories()

        assert [c.categoryName for c in sync_r.Response.categories] == [c.categoryName for c in async_r.Response.categories]
        print('GetTrendingCategories: OK')

    async def test_get_trending_category(self) -> None:
        category_id = 'News'
        page = 1

        sync_r = self.sync_client.trending.get_trending_category(
            category_id=category_id,
            page_number=page,
        )
        async_r = await self.async_client.trending.get_trending_category(
            category_id=category_id,
            page_number=page,
        )

        assert sync_r.Response.results[0].displayName == async_r.Response.results[0].displayName
        print('GetTrendingCategory: OK')

    async def test_get_trending_entry_detail(self) -> None:
        entry_type = TrendingEntryType.News
        identifier = 51515

        sync_r = self.sync_client.trending.get_trending_entry_detail(
            identifier=identifier,
            trending_entry_type=entry_type
        )
        async_r = await self.async_client.trending.get_trending_entry_detail(
            identifier=identifier,
            trending_entry_type=entry_type,
        )

        assert sync_r == async_r
        print('GetTrendingEntryDetail: OK')


class TestFireteam(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [ ] Fireteam.GetActivePrivateClanFireteamCount: Requires OAuth.
    - [ ] Fireteam.GetAvailableClanFireteams: Requires OAuth.
    - [ ] Fireteam.SearchPublicAvailableClanFireteams: Requires OAuth.
    - [ ] Fireteam.GetMyClanFireteams: Requires OAuth.
    - [ ] Fireteam.GetClanFireteam: Requires OAuth.
    """
    tests = []


class TestSocial(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [ ] Social.GetFriendList: Requires OAuth
    - [ ] Social.GetFriendRequestList: Requires OAuth
    - [ ] Social.IssueFriendRequest: Requires OAuth
    - [ ] Social.AcceptFriendRequest: Requires OAuth
    - [ ] Social.DeclineFriendRequest: Requires OAuth
    - [ ] Social.RemoveFriend: Requires OAuth
    - [ ] Social.RemoveFriendRequest: Requires OAuth
    - [ ] Social.GetPlatformFriendList: Requires OAuth
    """
    tests = []

    """
    async def test_get_platform_friend_list(self) -> None:
        friend_platform = PlatformFriendType.Steam
        page = 0

        sync_r = self.sync_client.social.get_platform_friend_list(
            friend_platform=friend_platform,
            page=page,
        )
        async_r = self.async_client.social.get_platform_friend_list(
            friend_platform=friend_platform,
            page=page,
        )

        assert sync_r == async_r
        print('GetPlatformFriendList: OK')
    """


class TestCore(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [x] Core.GetAvailableLocales
    - [x] Core.GetCommonSettings
    - [x] Core.GetUserSystemOverrides
    - [x] Core.GetGlobalAlerts
    """
    tests = [
        'test_get_available_locales',
        'test_get_common_settings',
        'test_get_user_system_overrides',
        'test_get_global_alerts',
    ]

    async def test_get_available_locales(self) -> None:
        sync_r = self.sync_client.core.get_available_locales()
        async_r = await self.async_client.core.get_available_locales()

        assert sync_r == async_r
        print('GetAvailableLocales: OK')

    async def test_get_common_settings(self) -> None:
        sync_r = self.sync_client.core.get_common_settings()
        async_r = await self.async_client.core.get_common_settings()

        assert sync_r == async_r
        print('GetCommonSettings: OK')

    async def test_get_user_system_overrides(self) -> None:
        sync_r = self.sync_client.core.get_user_system_overrides()
        async_r = await self.async_client.core.get_user_system_overrides()

        assert sync_r.ErrorCode == async_r.ErrorCode == PlatformErrorCodes.Success
        print('GetuserSystemOverrides: OK')

    async def test_get_global_alerts(self) -> None:
        include_streaming = True

        sync_r = self.sync_client.core.get_global_alerts(include_streaming)
        async_r = await self.async_client.core.get_global_alerts(include_streaming)

        assert sync_r == async_r
        print('GetGlobalAlerts: OK')


if __name__ == "__main__":
    TestApp.run_test()
    TestUser.run_test()
    TestContent.run_test()
    TestForum.run_test()
    TestForum.run_test()
    TestGroupV2.run_test()
    TestTokens.run_test()
    TestDestiny2.run_test()
    TestCommunityContent.run_test()
    TestTrending.run_test()
    TestFireteam.run_test()
    TestSocial.run_test()
    TestCore.run_test()

    # unittest.main()
