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

        # Get the data
        data = response.json

        # Assert the number of upvoters
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for user in data:
            self.assertIn('id', user)
            self.assertIn('username', user)
            self.assertIn('email', user)
            self.assertIn('following', user)
            self.assertIn('follower', user)
            self.assertIn('stats', user)
            self.assertIn('created_at', user)
            self.assertIn('updated_at', user)

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

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of upvotes
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for upvoter in data:
            self.assertIn('id', upvoter)
            self.assertIn('username', upvoter)
            self.assertIn('email', upvoter)
            self.assertIn('following', upvoter)
            self.assertIn('follower', upvoter)
            self.assertIn('stats', upvoter)
            self.assertIn('created_at', upvoter)
            self.assertIn('updated_at', upvoter)

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

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of upvotes
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
        for upvoter in data:
            self.assertIn('id', upvoter)
            self.assertIn('username', upvoter)
            self.assertIn('email', upvoter)
            self.assertIn('following', upvoter)
            self.assertIn('follower', upvoter)
            self.assertIn('stats', upvoter)
            self.assertIn('created_at', upvoter)
            self.assertIn('updated_at', upvoter)

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

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of upvotes
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
        for upvoter in data:
            self.assertIn('id', upvoter)
            self.assertIn('username', upvoter)
            self.assertIn('email', upvoter)
            self.assertIn('following', upvoter)
            self.assertIn('follower', upvoter)
            self.assertIn('stats', upvoter)
            self.assertIn('created_at', upvoter)
            self.assertIn('updated_at', upvoter)

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

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of upvotes
        self.assertEqual(len(data), n - b - c)

        # Assert the response data structure
        for upvoter in data:
            self.assertIn('id', upvoter)
            self.assertIn('username', upvoter)
            self.assertIn('email', upvoter)
            self.assertIn('following', upvoter)
            self.assertIn('follower', upvoter)
            self.assertIn('stats', upvoter)
            self.assertIn('created_at', upvoter)
            self.assertIn('updated_at', upvoter)

    def test_read_comment_upvoters_empty(self):
        # Create a comment
        comment = CommentFactory()

        # Get the upvoters
        response = self.client.get(self.route.format(comment.id))

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert the number of upvoters
        self.assertEqual(len(data), 0)

    def test_read_comment_upvoters_nonexistent(self):
        # Get the upvoters
        response = self.client.get(self.route.format(404))

        # Check status code
        self.assertEqual(response.status_code, 404)
