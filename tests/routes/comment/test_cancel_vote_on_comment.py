# Base
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory
from tests.factories.comment_factory import CommentFactory

# Utils
from tests.utils.tokens import get_access_token

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityBan


class TestCancelVoteOnComment(TestRoute):
    route = '/comment/{}/vote/cancel'

    def test_cancel_vote_on_comment(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the comment's community's subscribers
        community = comment.post.community
        CommunitySubscriber(community=community, user=user).save()

        # Create a vote on the comment
        CommentVoteFactory(user=user, comment=comment, direction=1)

        # Get the access token
        access_token = get_access_token(user)

        # Upvote the comment
        response = self.POSTRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 204)

    def test_cancel_vote_on_comment_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Cancel the vote on the comment
        response = self.POSTRequest(self.route.format(404), token=access_token)

        # Check status code
        self.assertStatusCode(response, 404)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Comment not found.')

    def test_cancel_vote_on_comment_being_banned(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the comment's community's banned
        community = comment.post.community
        CommunityBan(community=community, user=user).save()

        # Create a vote on the comment
        CommentVoteFactory(user=user, comment=comment, direction=1)

        # Get the access token
        access_token = get_access_token(user)

        # Cancel the vote on the comment
        response = self.POSTRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are banned from this community.')

    def test_cancel_vote_on_comment_not_being_subscribed(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Create a vote on the comment
        CommentVoteFactory(user=user, comment=comment, direction=1)

        # Get the access token
        access_token = get_access_token(user)

        # Cancel the vote on the comment
        response = self.POSTRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are not subscribed to this community.')

    def test_cancel_vote_on_comment_not_voted(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the comment's community's subscribers
        community = comment.post.community
        CommunitySubscriber(community=community, user=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Cancel the vote on the comment
        response = self.POSTRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You have not voted on this comment.')