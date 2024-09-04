# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token
from tests.utils.assert_pagination import assert_pagination_structure_comments
from tests.utils.assert_list import assert_comment_list


class TestDeleteComment(BaseTestCase):
    route = '/comment/'

    def test_read_comments(self):
        # Number of comments
        n = 5

        # Create multiple comments
        comments = CommentFactory.create_batch(size=n)

        # Get the comments
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments
        assert_comment_list(self, comments, expected_count=n)

    def test_read_comments_args(self):
        # Number of comments
        n = 5

        # Create multiple comments
        comments = CommentFactory.create_batch(size=n)

        # Get the comments
        response = self.client.get(
            self.route,
            query_string={'page': 1, 'per_page': 10}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=5
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments
        assert_comment_list(self, comments, expected_count=n)

    def test_read_comments_authenticated(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create multiple comments
        comments = CommentFactory.create_batch(size=n)

        # Get user access token
        access_token = get_access_token(user)

        # Get the comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments
        assert_comment_list(self, comments, expected_count=n)
    
    def test_read_comments_authenticated_args(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create multiple comments
        comments = CommentFactory.create_batch(size=n)

        # Get user access token
        access_token = get_access_token(user)

        # Get the comments
        response = self.client.get(
            self.route,
            query_string={'page': 1, 'per_page': 10},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments
        assert_comment_list(self, comments, expected_count=n)

    def test_read_comments_with_blocked(self):
        # Number of comments
        n = 5

        # Create multiple comments
        comments = CommentFactory.create_batch(n)

        # Number of blocked users
        b = 2

        # Create a user
        user = UserFactory()

        # Block some users
        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments
        assert_comment_list(self, comments, expected_count=n - b)

    def test_read_comments_with_blocked_args(self):
        # Number of comments
        n = 5

        # Create multiple comments
        comments = CommentFactory.create_batch(n)

        # Number of blocked users
        b = 2

        # Create a user
        user = UserFactory()

        # Block some users
        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the comments
        response = self.client.get(
            self.route,
            query_string={'page': 1, 'per_page': 10},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments
        assert_comment_list(self, comments, expected_count=n - b)

    def test_read_comments_with_blockers(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Number of blocked users
        b = 2

        for comment in comments[:b]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments
        assert_comment_list(self, comments, expected_count=n - b)

    def test_read_comments_with_blockers_args(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Number of blocked users
        b = 2

        for comment in comments[:b]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the comments
        response = self.client.get(
            self.route,
            query_string={'page': 1, 'per_page': 10},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments
        assert_comment_list(self, comments, expected_count=n - b)

    def test_read_comments_with_blocked_and_blockers(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Number of blocked users
        b = 2

        # Block some users
        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Number of blockers
        c = 2

        # Block some users
        for comment in comments[-c:]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b - c
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments
        assert_comment_list(self, comments, expected_count=n - b - c)

    def test_read_comments_with_blocked_and_blockers_args(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Number of blocked users
        b = 2

        # Block some users
        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Number of blockers
        c = 2

        # Block some users
        for comment in comments[-c:]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the comments
        response = self.client.get(
            self.route,
            query_string={'page': 1, 'per_page': 10},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b - c
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments
        assert_comment_list(self, comments, expected_count=n - b - c)

    def test_read_comments_empty(self):
        # Get the comments
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=10,
            expected_total=0
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments
        assert_comment_list(self, comments)

    def test_read_comments_empty_args(self):
        # Get the comments
        response = self.client.get(
            self.route,
            query_string={'page': 1, 'per_page': 10}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=10,
            expected_total=0
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments
        assert_comment_list(self, comments)

