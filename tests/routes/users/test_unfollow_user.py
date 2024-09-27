# tests
from tests.routes.test_route import TestRoute

# factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow

# utils
from tests.utils.tokens import get_access_token


class TestUnfollowUser(TestRoute):
    route = '/user/{}/unfollow'

    def test_unfollow_user(self):
        # Create a users
        user1 = UserFactory()

        # Create a user to follow
        user2 = UserFactory()

        # User1 follows user2
        Follow(follower=user1, followed=user2).save()

        # Get access token for user1
        access_token = get_access_token(user1)

        # User1 unfollows user2
        response = self.POSTRequest(self.route.format(user2.username), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 204)

    def test_unfollow_user_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get access token for the user
        access_token = get_access_token(user)

        # Try to unfollow a nonexistent user
        response = self.POSTRequest(self.route.format('nonexistent'), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 404)

        # Assert the response message
        self.assertMessage(response, 'User not found.')

    def test_unfollow_user_not_followed(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to follow
        user2 = UserFactory()

        # Get access token for user1
        access_token = get_access_token(user1)

        # Try to unfollow user2 without following them
        response = self.POSTRequest(self.route.format(user2.username), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 400)

        # Assert the response message
        self.assertMessage(response, 'You are not following this user.')

    def test_unfollow_user_self(self):
        # Create a user
        user = UserFactory()

        # Get access token for the user
        access_token = get_access_token(user)

        # Try to unfollow oneself
        response = self.POSTRequest(self.route.format(user.username), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 400)

        # Assert the response message
        self.assertMessage(response, 'You cannot unfollow yourself.')