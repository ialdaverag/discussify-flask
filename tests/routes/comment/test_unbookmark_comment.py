# Base
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory
from tests.factories.comment_bookmark_factory import CommentBookmarkFactory

# Utils
from tests.utils.tokens import get_access_token


class TestUnbookmarkComment(TestRoute):
    route = '/comment/{}/unbookmark'

    def test_unbookmark_comment(self):
        # Create a bookmarked comment
        bookmark = CommentBookmarkFactory()

        # Get the comment
        comment = bookmark.comment

        # Get the user
        user = bookmark.user

        # Get the access token
        access_token = get_access_token(user)

        # Unbookmark the comment
        response = self.POSTRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 204)

    def test_unbookmark_comment_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Unbookmark the comment
        response = self.POSTRequest(self.route.format(404), token=access_token)

        # Check status code
        self.assertStatusCode(response, 404)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Comment not found.')

    def test_unbookmark_comment_not_bookmarked(self):
        # Create a comment
        comment = CommentFactory()

        # Get the user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Unbookmark the comment
        response = self.POSTRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Comment not bookmarked.')