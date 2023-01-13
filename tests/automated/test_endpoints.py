import unittest

from generated.entities import ForumTopicsQuickDateEnum, ForumTopicsSortEnum, ForumTopicsCategoryFiltersEnum, \
    ForumPostSortEnum
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


if __name__ == "__main__":
    tests = {
        'APP': TestApp.suite(),
        'USER': TestUser.suite(),
        'CONTENT': TestContent.suite(),
        'FORUM': TestForum.suite(),
    }

    for name, test in tests.items():
        print(f' {name} TESTS '.center(100, '='))
        unittest.TextTestRunner().run(test)

    # unittest.main()
