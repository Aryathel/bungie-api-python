import unittest

from generated.entities import ForumTopicsQuickDateEnum, ForumTopicsSortEnum, ForumTopicsCategoryFiltersEnum, \
    ForumPostSortEnum, GroupType, BungieMembershipType, GroupsForMemberFilter, DestinyComponentType
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
        print('GetBungieApplications:', sync_r)


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
        print('GetBungieNetUserById:', sync_r)

    async def test_get_sanitized_platform_display_names(self) -> None:
        membership_id = 19548659
        sync_r = self.sync_client.user.get_sanitized_platform_display_names(membership_id)
        async_r = await self.async_client.user.get_sanitized_platform_display_names(membership_id)
        assert sync_r == async_r
        print('GetSanitizedPlatformDisplayNames:', sync_r)

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
        print('GetAvailableThemes:', sync_r)

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
        print('GetMembershipDataById:', sync_r)

    async def test_get_membership_from_hard_linked_credential(self) -> None:
        credential = '76561198119241330'
        cr_type = 12
        sync_r = self.sync_client.user.get_membership_from_hard_linked_credential(credential, cr_type)
        async_r = await self.async_client.user.get_membership_from_hard_linked_credential(credential, cr_type)
        assert sync_r == async_r
        print('GetMembershipFromHardLinkedCredential:', sync_r)

    async def test_search_by_global_name_post(self) -> None:
        page = 0
        display_name_prefix = 'Aryathel'
        sync_r = self.sync_client.user.search_by_global_name_post(display_name_prefix=display_name_prefix, page=page)
        async_r = await self.async_client.user.search_by_global_name_post(
            display_name_prefix=display_name_prefix,
            page=page
        )
        assert async_r == sync_r
        print('SearchByGlobalNamePost:', sync_r)


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
        print('GetContentType:', sync_r)

    async def test_get_content_by_id(self) -> None:
        c_id = 51999
        locale = 'en'
        sync_r = self.sync_client.content.get_content_by_id(c_id, locale)
        async_r = await self.async_client.content.get_content_by_id(c_id, locale)
        assert sync_r == async_r
        print('GetContentById:', sync_r)

    async def test_get_content_by_tag_and_type(self) -> None:
        locale = 'en'
        tag = 'twab'
        type = 'news'
        sync_r = self.sync_client.content.get_content_by_tag_and_type(locale, tag, type)
        async_r = await self.async_client.content.get_content_by_tag_and_type(locale, tag, type)
        assert sync_r == async_r
        print('GetContentByTagAndType:', sync_r)

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
        print('SearchContentWithText:', async_r)

    async def test_search_content_by_tag_and_type(self) -> None:
        locale = 'en'
        tag = 'twab'
        ctype = 'News'
        currentpage = 1
        sync_r = self.sync_client.content.search_content_by_tag_and_type(locale, tag, ctype, currentpage)
        async_r = await self.async_client.content.search_content_by_tag_and_type(locale, tag, ctype, currentpage)
        assert sync_r == async_r
        print('SearchContentByTagAndType:', sync_r)

    async def test_search_help_articles(self) -> None:
        searchtext = 'multikill'
        size = 15
        sync_r = self.sync_client.content.search_help_articles(searchtext, size)
        async_r = await self.async_client.content.search_help_articles(searchtext, size)
        assert sync_r == async_r
        print('SearchHelpArticles:', sync_r)

    async def test_rss_news_articles(self) -> None:
        page_token = 0
        category_filter = None
        include_body = False
        sync_r = self.sync_client.content.rss_news_articles(page_token, category_filter, include_body)
        async_r = await self.async_client.content.rss_news_articles(page_token, category_filter, include_body)
        assert sync_r == async_r
        print('RssNewsArticles:', sync_r)


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
        print('GetTopicsPaged:', sync_r)

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
        print('GetCoreTopicsPaged:', sync_r)

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
        print('GetPostsThreadedPaged:', sync_r)

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
        print('GetPostsThreadedPagedFromChild:', sync_r)

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
        print('GetPostAndParent:', sync_r)

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
        print('GetPostAndParentAwaitingApproval:', sync_r)
    """

    """
    async def test_get_topic_for_content(self) -> None:
        content_id = 123

        sync_r = self.sync_client.forum.get_topic_for_content(content_id)
        async_r = await self.async_client.forum.get_topic_for_content(content_id)
        assert sync_r == async_r
        print('GetTopicForContent:', sync_r)
    """

    async def test_get_forum_tag_suggestions(self) -> None:
        partial_tag = '#destiny'
        sync_r = self.sync_client.forum.get_forum_tag_suggestions(partial_tag)
        async_r = await self.async_client.forum.get_forum_tag_suggestions(partial_tag)
        assert sync_r == async_r
        print('GetForumTagSuggestions:', sync_r)

    async def test_get_poll(self) -> None:
        topic_id = 262238856
        sync_r = self.sync_client.forum.get_poll(topic_id)
        async_r = await self.async_client.forum.get_poll(topic_id)
        assert sync_r == async_r
        print('GetPoll:', sync_r)

    """
    async def test_get_recruitment_thread_summaries(self) -> None:
        ids = [262240321]
        sync_r = self.sync_client.forum.get_recruitment_thread_summaries(ids)
        async_r = await self.async_client.forum.get_recruitment_thread_summaries(ids)
        assert sync_r == async_r
        print('GetRecruitmentThreadSummaries:', sync_r)
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
        print('GetAvailableAvatars:', sync_r)

    async def test_get_available_themes(self) -> None:
        sync_r = self.sync_client.group_v2.get_available_themes()
        async_r = await self.async_client.group_v2.get_available_themes()
        assert sync_r == async_r
        print('GetAvailableThemes:', sync_r)

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
        print('GroupSearch:', sync_r)

    async def test_get_group(self) -> None:
        group_id = 2603136
        sync_r = self.sync_client.group_v2.get_group(group_id)
        async_r = await self.async_client.group_v2.get_group(group_id)
        assert sync_r == async_r
        print('GetGroup:', sync_r)

    async def test_get_group_by_name(self) -> None:
        group_name = 'Slicing Squall'
        group_type = GroupType.Clan
        sync_r = self.sync_client.group_v2.get_group_by_name(group_name, group_type)
        async_r = await self.async_client.group_v2.get_group_by_name(group_name, group_type)
        assert sync_r == async_r
        print('GetGroupByName:', sync_r)

    async def test_get_group_by_name_v2(self) -> None:
        group_name = 'Slicing Squall'
        group_type = GroupType.Clan
        sync_r = self.sync_client.group_v2.get_group_by_name_v2(group_name, group_type)
        async_r = await self.async_client.group_v2.get_group_by_name_v2(group_name, group_type)
        assert sync_r == async_r
        print('GetGroupByNameV2:', sync_r)

    async def test_get_group_optional_conversations(self) -> None:
        group_id = 2603136
        sync_r = self.sync_client.group_v2.get_group_optional_conversations(group_id)
        async_r = await self.async_client.group_v2.get_group_optional_conversations(group_id)
        assert async_r == sync_r
        print('GetGroupOptionalConversations:', sync_r)

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
        print('GetMembersOfGroup:', sync_r)

    async def test_get_admins_and_founder_of_group(self) -> None:
        group_id = 2603136
        current_page = 1
        sync_r = self.sync_client.group_v2.get_admins_and_founder_of_group(current_page, group_id)
        async_r = await self.async_client.group_v2.get_admins_and_founder_of_group(current_page, group_id)
        assert sync_r == async_r
        print('GetAdminsAndFounderOfGroup:', sync_r)

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
        assert sync_r == async_r
        print('GetGroupsForMember:', sync_r)

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
        print('RecoverGroupForFounder:', sync_r)
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
        print('GetPotentialGroupsForMember:', sync_r)


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
        print('GetBungieRewardList:', sync_r)


class TestDestiny2(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [ ] Destiny2.GetDestinyManifest
    - [ ] Destiny2.GetDestinyEntityDefinition
    - [ ] Destiny2.SearchDestinyPlayerByBungieName
    - [ ] Destiny2.GetLinkedProfiles
    - [ ] Destiny2.GetProfile
    - [ ] Destiny2.GetCharacter
    - [ ] Destiny2.GetClanWeeklyRewardState
    - [ ] Destiny2.GetClanBannerSource
    - [ ] Destiny2.GetItem
    - [ ] Destiny2.GetVendors
    - [ ] Destiny2.GetVendor
    - [ ] Destiny2.GetPublicVendors Preview
    - [ ] Destiny2.GetCollectibleNodeDetails
    - [ ] Destiny2.TransferItem
    - [ ] Destiny2.PullFromPostmaster
    - [ ] Destiny2.EquipItem
    - [ ] Destiny2.EquipItems
    - [ ] Destiny2.SetItemLockState
    - [ ] Destiny2.SetQuestTrackedState
    - [ ] Destiny2.InsertSocketPlug Preview
    - [ ] Destiny2.InsertSocketPlugFree Preview
    - [ ] Destiny2.GetPostGameCarnageReport
    - [ ] Destiny2.ReportOffensivePostGameCarnageReportPlayer
    - [ ] Destiny2.GetHistoricalStatsDefinition
    - [ ] Destiny2.GetClanLeaderboards Preview
    - [ ] Destiny2.GetClanAggregateStats Preview
    - [ ] Destiny2.GetLeaderboards Preview
    - [ ] Destiny2.GetLeaderboardsForCharacter Preview
    - [ ] Destiny2.SearchDestinyEntities
    - [ ] Destiny2.GetHistoricalStats
    - [ ] Destiny2.GetHistoricalStatsForAccount
    - [ ] Destiny2.GetActivityHistory
    - [ ] Destiny2.GetUniqueWeaponHistory
    - [ ] Destiny2.GetDestinyAggregateActivityStats
    - [ ] Destiny2.GetPublicMilestoneContent
    - [ ] Destiny2.GetPublicMilestones
    - [ ] Destiny2.AwaInitializeRequest
    - [ ] Destiny2.AwaProvideAuthorizationResult
    - [ ] Destiny2.AwaGetActionToken
    """
    tests = [
        'test_get_destiny_manifest',
        'test_get_destiny_entity_definition',
        'test_search_destiny_player_by_bungie_name',
        'test_get_linked_profiles',
        'test_get_profile',
        'test_get_character',
    ]

    async def test_get_destiny_manifest(self) -> None:
        sync_r = self.sync_client.destiny2.get_destiny_manifest()
        async_r = await self.async_client.destiny2.get_destiny_manifest()
        assert sync_r == async_r
        print('GetDestinyManifest:', sync_r)

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
        print('GetDestinyEntityDefinition:', sync_r)

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
        print('SearchDestinyPlayerByBungieName:', sync_r)

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
        print('GetLinkedProfiles:', sync_r)

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
        print('GetCharacter:', sync_r)

    async def test_get_clan_weekly_reward_state(self) -> None:
        group_id = 2603136
        sync_r = self.sync_client.destiny2.get_clan_weekly_reward_state(group_id)
        async_r = await self.async_client.destiny2.get_clan_weekly_reward_state(group_id)
        assert sync_r == async_r
        print('GetClanWeeklyRewardState:', sync_r)


if __name__ == "__main__":
    tests = {
        'APP': TestApp.suite(),
        'USER': TestUser.suite(),
        'CONTENT': TestContent.suite(),
        'FORUM': TestForum.suite(),
        'GROUPV2': TestGroupV2.suite(),
        'TOKENS': TestTokens.suite(),
        'DESTINY2': TestDestiny2.suite(),
    }

    for name, test in tests.items():
        print(f' {name} TESTS '.center(100, '='))
        unittest.TextTestRunner().run(test)

    # unittest.main()
