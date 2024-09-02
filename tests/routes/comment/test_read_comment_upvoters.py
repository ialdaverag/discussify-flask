# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory
from tests.factories.comment_factory import CommentFactory

# Models
from app.models.user import Block

# Utils
from tests.utils.tokens import get_access_token
from tests.utils.assert_pagination import assert_pagination_structure
from tests.utils.assert_list import assert_user_list


class TestReadCommentUpvoters(BaseTestCase):
    route = '/comment/{}/upvoters'

    def test_read_comment_upvoters(self):
        # Number of upvoters
        n = 5

        # Create a comment
        comment = CommentFactory()

        # Create some upvoters
        CommentVoteFactory.create_batch(n, comment=comment, direction=1)

        # Get the upvoters
        response = self.client.get(self.route.format(comment.id))

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=1, 
            expected_per_page=10, 
            expected_total=n
        )

        # Get the upvoters
        upvoters = pagination['users']

        # Assert the upvoters list
        assert_user_list(self, upvoters, n)

    def test_read_comment_upvoters_args(self):
        # Number of upvoters
        n = 5

        # Create a comment
        comment = CommentFactory()

        # Create some upvoters
        CommentVoteFactory.create_batch(n, comment=comment, direction=1)

        # Get the upvoters
        response = self.client.get(
            self.route.format(comment.id),
            query_string={'page': 1, 'per_page': 5}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=1, 
            expected_per_page=5, 
            expected_total=n
        )

        # Get the upvoters
        upvoters = pagination['users']

        # Assert the upvoters list
        assert_user_list(self, upvoters, n)

    def test_read_commentt_upvoters_authenticated(self):
        # Number of upvoters
        n = 5

        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Create some upvoters
        CommentVoteFactory.create_batch(n, comment=comment, direction=1)

        # Get the access token
        access_token = get_access_token(user)

        # Get the upvoters
        response = self.client.get(
            self.route.format(comment.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=1, 
            expected_per_page=10, 
            expected_total=n
        )

        # Get the upvoters
        upvoters = pagination['users']

        # Assert the upvoters list
        assert_user_list(self, upvoters, n)

    def test_read_comment_upvoters_authenticated_args(self):
        # Number of upvoters
        n = 5

        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Create some upvoters
        CommentVoteFactory.create_batch(n, comment=comment, direction=1)

        # Get the access token
        access_token = get_access_token(user)

        # Get the upvoters
        response = self.client.get(
            self.route.format(comment.id),
            query_string={'page': 1, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=1, 
            expected_per_page=5, 
            expected_total=n
        )

        # Get the upvoters
        upvoters = pagination['users']

        # Assert the upvoters list
        assert_user_list(self, upvoters, n)

    def test_read_comment_upvoters_with_blocked(self):
        # Number of upvoters
        n = 5

        # Number of blocked upvoters
        b = 2

        # Create a comment
        comment = CommentFactory()

        # Create some upvoters
        upvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=1)

        # Create a user
        user = UserFactory()

        # Block the upvoters
        for upvoter in upvoters[:b]:
            Block(blocker=user, blocked=upvoter.user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the upvoters
        response = self.client.get(
            self.route.format(comment.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=1, 
            expected_per_page=10, 
            expected_total=n - b
        )

        # Get the upvoters
        upvoters = pagination['users']

        # Assert the upvoters list
        assert_user_list(self, upvoters, n - b)

    def test_read_comment_upvoters_with_blocked_args(self):
        # Number of upvoters
        n = 5

        # Number of blocked upvoters
        b = 2

        # Create a comment
        comment = CommentFactory()

        # Create some upvoters
        upvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=1)

        # Create a user
        user = UserFactory()

        # Block the upvoters
        for upvoter in upvoters[:b]:
            Block(blocker=user, blocked=upvoter.user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the upvoters
        response = self.client.get(
            self.route.format(comment.id),
            query_string={'page': 1, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=1, 
            expected_per_page=5, 
            expected_total=n - b
        )

        # Get the upvoters
        upvoters = pagination['users']

        # Assert the upvoters list
        assert_user_list(self, upvoters, n - b)

    def test_read_comment_upvoters_with_blockers(self):
        # Number of upvoters
        n = 5

        # Number of blockers
        b = 3

        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Create some upvoters
        upvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=1)

        # Block the user from the first 3 upvoters
        for upvoter in upvoters[:b]:
            Block(blocker=upvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the upvoters
        response = self.client.get(
            self.route.format(comment.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get the upvoters
        upvoters = pagination['users']

        # Assert the upvoters list
        assert_user_list(self, upvoters, n - b)

    def test_read_comment_upvoters_with_blockers_args(self):
        # Number of upvoters
        n = 5

        # Number of blockers
        b = 3

        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Create some upvoters
        upvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=1)

        # Block the user from the first 3 upvoters
        for upvoter in upvoters[:b]:
            Block(blocker=upvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the upvoters
        response = self.client.get(
            self.route.format(comment.id),
            query_string={'page': 1, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get the upvoters
        upvoters = pagination['users']

        # Assert the upvoters list
        assert_user_list(self, upvoters, n - b)

    def test_read_comment_upvoters_with_blocked_and_blockers(self):
        # Number of upvoters
        n = 5

        # Number of blocked upvoters
        b = 2

        # Number of blockers
        c = 2

        # Create a comment
        comment = CommentFactory()

        # Create some upvoters
        upvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=1)

        # Create a user
        user = UserFactory()

        # Block the upvoters
        for upvoter in upvoters[:b]:
            Block(blocker=user, blocked=upvoter.user).save()

        # Block the user
        for upvoter in upvoters[-c:]:
            Block(blocker=upvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the upvoters
        response = self.client.get(
            self.route.format(comment.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b - c
        )

        # Get the upvoters
        upvoters = pagination['users']

        # Assert the upvoters list
        assert_user_list(self, upvoters, n - b - c)

    def test_read_comment_upvoters_with_blocked_and_blockers_args(self):
        # Number of upvoters
        n = 5

        # Number of blocked upvoters
        b = 2

        # Number of blockers
        c = 2

        # Create a comment
        comment = CommentFactory()

        # Create some upvoters
        upvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=1)

        # Create a user
        user = UserFactory()

        # Block the upvoters
        for upvoter in upvoters[:b]:
            Block(blocker=user, blocked=upvoter.user).save()

        # Block the user
        for upvoter in upvoters[-c:]:
            Block(blocker=upvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the upvoters
        response = self.client.get(
            self.route.format(comment.id),
            query_string={'page': 1, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n - b - c
        )

        # Get the upvoters
        upvoters = pagination['users']

        # Assert the upvoters list
        assert_user_list(self, upvoters, n - b - c)

    def test_read_comment_upvoters_empty(self):
        # Create a comment
        comment = CommentFactory()

        # Get the upvoters
        response = self.client.get(self.route.format(comment.id))

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=10,
            expected_total=0
        )

        # Get the upvoters
        upvoters = pagination['users']

        # Assert the upvoters list
        assert_user_list(self, upvoters, 0)

    def test_read_comment_upvoters_empty_args(self):
        # Create a comment
        comment = CommentFactory()

        # Get the upvoters
        response = self.client.get(
            self.route.format(comment.id),
            query_string={'page': 1, 'per_page': 5}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=5,
            expected_total=0
        )

        # Get the upvoters
        upvoters = pagination['users']

        # Assert the upvoters list
        assert_user_list(self, upvoters, 0)

    def test_read_comment_upvoters_nonexistent(self):
        # Get the upvoters
        response = self.client.get(self.route.format(404))

        # Check status code
        self.assertEqual(response.status_code, 404)
