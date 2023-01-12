import unittest

from ..core import TestCore


class TestApp(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [ ] App.GetApplicationApiUsage: Requires OAuth
    - [x] App.GetApplicationApiUsage
    """
    async def test_get_bungie_applications(self) -> None:
        sync_r = self.sync_client.app.get_bungie_applications()
        async_r = await self.async_client.app.get_bungie_applications()
        assert sync_r == async_r


class TestUser(unittest.IsolatedAsyncioTestCase, TestCore):
    """
    Coverage:
    - [x] User.GetBungieNetUserById:
    - [x] User.GetSanitizedPlatformDisplayNames:
    - [ ] User.GetCredentialTypesForTargetAccount: Requires OAuth
    - [x] User.GetAvailableThemes:
    - [x] User.GetMembershipDataById:
    - [ ] User.GetMembershipDataForCurrentUser: Requires OAuth
    - [x] User.GetMembershipFromHardLinkedCredential:
    - [x] User.SearchByGlobalNamePrefix:
    """

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


if __name__ == "__main__":
    unittest.main()
