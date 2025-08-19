# Base
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory

# Utils
from tests.utils.tokens import get_access_token

# Models
from app.models.community import CommunityModerator


class TestDeleteComment(TestRoute):
    route = '/comment/{}'

    def test_delete_comment(self):
        # Create a comment
        comment = CommentFactory()

        # Get the owner of the comment
        owner = comment.owner

        # Get the access token
        access_token = get_access_token(owner)

        # Delete the comment
        response = self.DELETERequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 204)

    def test_delete_comment_as_moderator(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the community of the comment
        community = comment.post.community

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Delete the comment
        response = self.DELETERequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 204)

    def test_delete_comment_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Delete the comment
        response = self.DELETERequest(self.route.format(404), token=access_token)

        # Check status code
        self.assertStatusCode(response, 404)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Comment not found.')

    def test_delete_comment_not_being_owner(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Delete the comment
        response = self.DELETERequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 403)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You cannot delete this comment.')