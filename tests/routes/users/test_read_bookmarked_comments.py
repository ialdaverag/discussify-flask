# tests
from tests.base.base_pagination_test import BasePaginationTest

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_bookmark_factory import CommentBookmarkFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadBookmarkedComments(BasePaginationTest):
    route = '/user/comments/bookmarked'

    def test_read_bookmarked_comments(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        CommentBookmarkFactory.create_batch(n, user=user)

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response for comments
        self.assert_standard_pagination_response(response, expected_total=n, data_key='comments')

    def test_read_bookmarked_comments_args(self):
        # Number of comments
        n = 15

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        CommentBookmarkFactory.create_batch(n, user=user)

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
        response = self.GETRequest(f'{self.route}?page=1&per_page=5', token=access_token)

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=5,
            expected_total=n,
            data_key='comments'
        )

    def test_read_bookmarked_comments_with_blocked(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = CommentBookmarkFactory.create_batch(n, user=user)

        # Number of blocked users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=user, blocked=bookmark.comment.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n - b, data_key='comments')

    def test_read_bookmarked_comments_with_blocked_args(self):
        # Number of comments
        n = 15

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = CommentBookmarkFactory.create_batch(n, user=user)

        # Number of blocked users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=user, blocked=bookmark.comment.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
        response = self.GETRequest(f'{self.route}?page=1&per_page=5', token=access_token)

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=5,
            expected_total=n - b,
            data_key='comments'
        )

    def test_read_bookmarked_comments_with_blockers(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = CommentBookmarkFactory.create_batch(n, user=user)

        # Number of blocking users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=bookmark.comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n - b, data_key='comments')

    def test_read_bookmarked_comments_with_blockers_args(self):
        # Number of comments
        n = 15

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = CommentBookmarkFactory.create_batch(n, user=user)

        # Number of blocking users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=bookmark.comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
        response = self.GETRequest(f'{self.route}?page=1&per_page=5', token=access_token)

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=5,
            expected_total=n - b,
            data_key='comments'
        )

    def test_read_bookmarked_comments_with_blocked_and_blockers(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = CommentBookmarkFactory.create_batch(n, user=user)

        # Number of blocking users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=bookmark.comment.owner, blocked=user).save()

        # Number of blocked users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=user, blocked=bookmark.comment.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n - b, data_key='comments')

    def test_read_bookmarked_comments_with_blocked_and_blockers_args(self):
        # Number of comments
        n = 15

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = CommentBookmarkFactory.create_batch(n, user=user)

        # Number of blocking users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=bookmark.comment.owner, blocked=user).save()

        # Number of blocked users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=user, blocked=bookmark.comment.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
        response = self.GETRequest(f'{self.route}?page=1&per_page=5', token=access_token)

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=5,
            expected_total=n - b,
            data_key='comments'
        )

    def test_read_bookmarked_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response with 0 total
        self.assert_standard_pagination_response(response, expected_total=0, data_key='comments')

    def test_read_bookmarked_comments_empty_args(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
        response = self.GETRequest(f'{self.route}?page=1&per_page=5', token=access_token)

        # Assert paginated response with 0 total
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=5,
            expected_total=0,
            data_key='comments'
        )