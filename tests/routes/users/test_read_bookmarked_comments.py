# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_bookmark_factory import CommentBookmarkFactory
from tests.factories.user_factory import UserFactory
from tests.factories.block_factory import BlockFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token
from tests.utils.assert_pagination import assert_pagination_structure_comments
from tests.utils.assert_list import assert_comment_list


class TestReadBookmarkedComments(BaseTestCase):
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
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get pagination data
        pagination = response.json

         # Assert pagination data structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get comments
        comments = pagination['comments']

        # Assert comments list
        assert_comment_list(self, comments, n)

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
        response = self.client.get(
            f'{self.route}?page=1&per_page=5',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get pagination data
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n
        )

        # Get comments
        comments = pagination['comments']

        # Assert comments list
        assert_comment_list(self, comments, 5)

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
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get comments
        comments = pagination['comments']

        # Assert comments list
        assert_comment_list(self, comments, n - b)

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
        response = self.client.get(
            f'{self.route}?page=1&per_page=5',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get comments
        comments = pagination['comments']

        # Assert comments list
        assert_comment_list(self, comments, 5)

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
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get comments
        comments = pagination['comments']

        # Assert comments list
        assert_comment_list(self, comments, n - b)

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
        response = self.client.get(
            f'{self.route}?page=1&per_page=5',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get comments
        comments = pagination['comments']

        # Assert comments list
        assert_comment_list(self, comments, 5)

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
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get comments
        comments = pagination['comments']

        # Assert comments list
        assert_comment_list(self, comments, n - b)

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
        response = self.client.get(
            f'{self.route}?page=1&per_page=5',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get comments
        comments = pagination['comments']

        # Assert comments list
        assert_comment_list(self, comments, 5)

    def test_read_bookmarked_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=10,
            expected_total=0
        )

        # Get comments
        comments = pagination['comments']

        # Assert comments list
        assert_comment_list(self, comments)

    def test_read_bookmarked_comments_empty_args(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked comments
        response = self.client.get(
            f'{self.route}?page=1&per_page=5',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=5,
            expected_total=0
        )

        # Get comments
        comments = pagination['comments']

        # Assert comments list
        assert_comment_list(self, comments)