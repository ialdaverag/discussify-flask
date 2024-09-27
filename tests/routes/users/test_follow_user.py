# Tests
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestFollowUser(TestRoute):
    route = '/user/{}/follow'

    def test_follow_user(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to follow
        user2 = UserFactory()

        # Get access token for user1
        access_token = get_access_token(user1)

        # User1 follows user2
        response = self.POSTRequest(self.route.format(user2.username), token=access_token)

        # Assert that the response status code is 204 (No Content)
        self.assertStatusCode(response, 204)

    def test_follow_user_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get access token for the user
        access_token = get_access_token(user)

        # Try to follow a nonexistent user
        response = self.POSTRequest(self.route.format('nonexistent'), token=access_token)

        # Assert response status
        self.assertStatusCode(response, 404)

        # Assert response message
        self.assertMessage(response, 'User not found.')

    def test_follow_target_blocked_by_user(self):
        # Create two users
        user1 = UserFactory()
        user2 = UserFactory()

        # User2 blocks user1
        Block(blocker=user1, blocked=user2).save()

        # Get access token for user1
        access_token = get_access_token(user1)

        # Try to follow user2
        response = self.POSTRequest(self.route.format(user2.username), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 400)

        # Assert response message
        self.assertMessage(response, 'You cannot follow this user.')

    def test_follow_user_blocked_by_target(self):
        # Create two users
        user1 = UserFactory()
        user2 = UserFactory()

        # User1 blocks user2
        Block(blocker=user2, blocked=user1).save()

        # Get access token for user1
        access_token = get_access_token(user1)

        # Try to follow user2
        response = self.POSTRequest(self.route.format(user2.username), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 400)

        # Assert response message
        self.assertMessage(response, 'You cannot follow this user.')

    def test_follow_user_already_followed(self):
        # Create two users
        user1 = UserFactory()
        user2 = UserFactory()

        # Get access token for user1
        access_token = get_access_token(user1)

        # User1 follows user2
        Follow(follower=user1, followed=user2).save()

        # Try to follow user2 again
        response = self.POSTRequest(self.route.format(user2.username), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 400)

        # Assert response message
        self.assertMessage(response, 'You are already following this user.')

    def test_follow_user_self(self):
        # Create a user
        user = UserFactory()

        # Get access token for the user
        access_token = get_access_token(user)

        # Try to follow oneself
        response = self.POSTRequest(self.route.format(user.username), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 400)

        # Assert response message
        self.assertMessage(response, 'You cannot follow yourself.')
