# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_vote_factory import CommentVoteFactory
from tests.factories.comment_factory import CommentFactory
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Block

# Utils
from tests.utils.tokens import get_access_token


class TestReadCommentDownvoters(BaseTestCase):
    route = '/comment/{}/downvoters'

    def test_read_comment_downvoters(self):
        # Number of downvoters
        n = 5

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Get the downvoters
        response = self.client.get(self.route.format(comment.id))

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert the number of downvoters
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

    def test_read_commentt_downvoters_authenticated(self):
        # Number of downvoters
        n = 5

        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
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

        # Assert the number of downvotes
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for downvoter in data:
            self.assertIn('id', downvoter)
            self.assertIn('username', downvoter)
            self.assertIn('email', downvoter)
            self.assertIn('following', downvoter)
            self.assertIn('follower', downvoter)
            self.assertIn('stats', downvoter)
            self.assertIn('created_at', downvoter)
            self.assertIn('updated_at', downvoter)

    def test_read_comment_downvoters_with_blocked(self):
        # Number of downvoters
        n = 5

        # Number of blocked downvoters
        b = 2

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        downvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Create a user
        user = UserFactory()

        # Block the downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=user, blocked=downvoter.user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
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

        # Assert the number of downvotes
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
        for downvoter in data:
            self.assertIn('id', downvoter)
            self.assertIn('username', downvoter)
            self.assertIn('email', downvoter)
            self.assertIn('following', downvoter)
            self.assertIn('follower', downvoter)
            self.assertIn('stats', downvoter)
            self.assertIn('created_at', downvoter)
            self.assertIn('updated_at', downvoter)

    def test_read_comment_downvoters_with_blockers(self):
        # Number of downvoters
        n = 5

        # Number of blockers
        b = 3

        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        downvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Block the user from the first 3 downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=downvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
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

        # Assert the number of downvotes
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
        for downvoter in data:
            self.assertIn('id', downvoter)
            self.assertIn('username', downvoter)
            self.assertIn('email', downvoter)
            self.assertIn('following', downvoter)
            self.assertIn('follower', downvoter)
            self.assertIn('stats', downvoter)
            self.assertIn('created_at', downvoter)
            self.assertIn('updated_at', downvoter)

    def test_read_comment_downvoters_with_blocked_and_blockers(self):
        # Number of upvoters
        n = 5

        # Number of blocked upvoters
        b = 2

        # Number of blockers
        c = 2

        # Create a comment
        comment = CommentFactory()

        # Create some upvoters
        downvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Create a user
        user = UserFactory()

        # Block the downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=user, blocked=downvoter.user).save()

        # Block the user
        for downvoter in downvoters[-c:]:
            Block(blocker=downvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
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

        # Assert the number of downvotes
        self.assertEqual(len(data), n - b - c)

        # Assert the response data structure
        for downvoter in data:
            self.assertIn('id', downvoter)
            self.assertIn('username', downvoter)
            self.assertIn('email', downvoter)
            self.assertIn('following', downvoter)
            self.assertIn('follower', downvoter)
            self.assertIn('stats', downvoter)
            self.assertIn('created_at', downvoter)
            self.assertIn('updated_at', downvoter)

    def test_read_comment_downvoters_empty(self):
        # Create a comment
        comment = CommentFactory()

        # Get the downvoters
        response = self.client.get(self.route.format(comment.id))

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert the number of downvoters
        self.assertEqual(len(data), 0)

    def test_read_comment_downvoters_nonexistent(self):
        # Get the downvoters
        response = self.client.get(self.route.format(404))

        # Check status code
        self.assertEqual(response.status_code, 404)
