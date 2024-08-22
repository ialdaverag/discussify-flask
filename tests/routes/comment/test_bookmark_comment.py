# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory
from tests.factories.comment_bookmark_factory import CommentBookmarkFactory

# Models
from app.models.user import Block

# Utils
from tests.utils.tokens import get_access_token


class TestBookmarkComment(BaseTestCase):
    route = '/comment/{}/bookmark'

    def test_bookmark_post(self):
        # Create a comment
        comment = CommentFactory()

        # Get the user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Bookmark the comment
        response = self.client.post(
            self.route.format(comment.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 204)

    def test_bookmark_comment_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Bookmark the comment
        response = self.client.post(
            self.route.format(1),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 404)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Comment not found.')

    def test_bookmark_comment_owner_blocked_by_user(self):
        # Create a comment
        comment = CommentFactory()

        # Get the user
        user = UserFactory()

        # Get the comment's owner
        owner = comment.owner

        # Block the comment's owner
        Block(blocker=user, blocked=owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Bookmark the comment
        response = self.client.post(
            self.route.format(comment.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You cannot bookmark this comment.')

    def test_bookmark_comment_user_blocked_by_owner(self):
        # Create a comment
        comment = CommentFactory()

        # Get the user
        user = UserFactory()

        # Get the comment's owner
        owner = comment.owner

        # Block the user
        Block(blocker=owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Bookmark the comment
        response = self.client.post(
            self.route.format(comment.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You cannot bookmark this comment.')

    def test_bookmark_comment_already_bookmarked(self):
        # Create a bookmarked comment
        bookmark = CommentBookmarkFactory()

        # Get the comment
        comment = bookmark.comment

        # Get the user
        user = bookmark.user

        # Get the access token
        access_token = get_access_token(user)

        # Bookmark the comment again
        response = self.client.post(
            self.route.format(comment.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Comment already bookmarked.')
