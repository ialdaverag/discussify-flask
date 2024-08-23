# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Block

# Utils
from tests.utils.tokens import get_access_token


class TestReadComment(BaseTestCase):
    route = '/comment/{}'

    def test_read_comment_anonymous(self):
        # Create a comment
        comment = CommentFactory()

        # Read the comment
        response = self.client.get(self.route.format(comment.id))

        # Assert the status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert keys in data
        self.assertIn('id', data)
        self.assertIn('content', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

        # Assert that the comment data is correct
        self.assertEqual(data['id'], comment.id)
        self.assertEqual(data['content'], comment.content)
        self.assertEqual(data['created_at'], comment.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(data['updated_at'], comment.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_read_comment(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Read the comment
        response = self.client.get(
            self.route.format(comment.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert keys in data
        self.assertIn('id', data)
        self.assertIn('content', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

        # Assert that the comment data is correct
        self.assertEqual(data['id'], comment.id)
        self.assertEqual(data['content'], comment.content)
        self.assertEqual(data['created_at'], comment.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(data['updated_at'], comment.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_read_comment_user_blocked_by_owner(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the owner of the comment
        owner = comment.owner

        # Block the user
        Block(blocker=owner, blocked=user).save()

         # Get the access token
        access_token = get_access_token(user)

        # Read the post
        response = self.client.get(
            self.route.format(comment.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the status code
        self.assertEqual(response.status_code, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You cannot view this comment.')

    def test_read_comment_user_owner_blocked_by_user(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the owner of the comment
        owner = comment.owner

        # Block the owner
        Block(blocker=user, blocked=owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Read the post
        response = self.client.get(
            self.route.format(comment.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the status code
        self.assertEqual(response.status_code, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You cannot view this comment.')

    def test_read_comment_nonexistent(self):
        # Read the comment
        response = self.client.get(self.route.format(404))

        # Assert the status code
        self.assertEqual(response.status_code, 404)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Comment not found.')