# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory

# Models
from app.models.comment import CommentVote

# utils
from tests.utils.tokens import get_access_token
from tests.utils.assert_pagination import assert_pagination_structure_comments
from tests.utils.assert_list import assert_comment_list

# Models
from app.models.user import Block


class TestReadDownvotedComments(BaseTestCase):
    route = '/user/comments/downvoted'

    def test_read_downvoted_comments(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user downvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=-1).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user downvoted comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
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

        # Assert the comments list
        assert_comment_list(self, comments, n)

    def test_read_downvoted_comments_args(self):
        # Number of comments
        n = 15

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user downvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=-1).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user downvoted comments
        response = self.client.get(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=2,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments list
        assert_comment_list(self, comments, 5)

    def test_read_downvoted_comments_with_blocked(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user downvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=-1).save()

        # Number of blocked users
        b = 2

        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user downvoted comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
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

        # Assert the comments list
        assert_comment_list(self, comments, n - b)

    def test_read_downvoted_comments_with_blocked_args(self):
        # Number of comments
        n = 15

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user downvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=-1).save()

        # Number of blocked users
        b = 2

        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user downvoted comments
        response = self.client.get(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=2,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments list
        assert_comment_list(self, comments, 5)

    def test_read_downvoted_comments_with_blockers(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user downvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=-1).save()

        # Number of blocking users
        b = 2

        for comment in comments[:b]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user downvoted comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
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

        # Assert the comments list
        assert_comment_list(self, comments, n - b)

    def test_read_downvoted_comments_with_blockers_args(self):
        # Number of comments
        n = 15

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user downvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=-1).save()

        # Number of blocking users
        b = 2

        for comment in comments[:b]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user downvoted comments
        response = self.client.get(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=2,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments list
        assert_comment_list(self, comments, 5)

    def test_read_downvoted_comments_with_blocked_and_blockers(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user downvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=-1).save()

        # Number of blocked users
        b = 2

        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Number of blockers users
        c = 2

        for comment in comments[-c:]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user downvoted comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
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

        # Assert the comments list
        assert_comment_list(self, comments, n - b - c)

    def test_read_downvoted_comments_with_blocked_and_blockers_args(self):
        # Number of comments
        n = 15

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user downvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=-1).save()

        # Number of blocked users
        b = 2

        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Number of blockers users
        c = 2

        for comment in comments[-c:]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user downvoted comments
        response = self.client.get(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=2,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b - c
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments list
        assert_comment_list(self, comments, 5)

    def test_read_downvoted_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user downvoted comments
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
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

        # Assert the comments list
        assert_comment_list(self, comments)

    def test_read_downvoted_comments_empty_args(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user downvoted comments
        response = self.client.get(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=2,
            expected_pages=0,
            expected_per_page=5,
            expected_total=0
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments list
        assert_comment_list(self, comments)