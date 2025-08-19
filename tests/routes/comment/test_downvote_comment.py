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
from app.models.user import Block


class TestDownvoteComment(TestRoute):
    route = '/comment/{}/vote/down'

    def test_downvote_comment(self):
        # Create a post
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the post's community's subscribers
        community = comment.post.community
        CommunitySubscriber(community=community, user=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Downvote the comment
        response = self.POSTRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 204)

    def test_downvote_comment_owner_blocked_by_user(self):
        # Create a post
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the post's
        community = comment.post.community

        # Append the user to the post's community's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Get the post's owner
        owner = comment.owner

        # Block the post's owner
        Block(blocker=user, blocked=owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Downvote the comment
        response = self.POSTRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

    def test_downvote_comment_user_blocked_by_owner(self):
        # Create a post
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the post's
        community = comment.post.community

        # Append the user to the post's community's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Get the post's owner
        owner = comment.owner

        # Block the post's owner
        Block(blocker=owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Cownvote the comment
        response = self.POSTRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

    def test_downvote_comment_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Downvote the comment
        response = self.POSTRequest(self.route.format(404), token=access_token)

        # Check status code
        self.assertStatusCode(response, 404)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Comment not found.')

    def test_downvote_comment_being_banned(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the post's community's banned
        community = comment.post.community
        CommunityBan(community=community, user=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Downvote the post
        response = self.POSTRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are banned from this community.')

    def test_downvote_comment_being_not_subscribed(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Downvote the post
        response = self.POSTRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are not subscribed to this community.')

    def test_downvote_comment_already_downvoted(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the post's upvoters
        CommentVoteFactory(user=user, comment=comment, direction=-1)

        # Append the user to the post's community's subscribers
        community = comment.post.community
        CommunitySubscriber(community=community, user=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Downvote the post
        response = self.POSTRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You have already downvoted this post.')
    