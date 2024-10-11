# Tests
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow
from app.models.user import Block

# Utils
from tests.utils.tokens import get_access_token


class TestBlockUser(TestRoute):
    route = '/user/{}/block'

    def test_block_user(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to block
        user2 = UserFactory()

        # Get access token for user1
        access_token = get_access_token(user1)

        # User1 blocks user2
        response = self.POSTRequest(self.route.format(user2.username), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 204)

    def test_block_user_following(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to block
        user2 = UserFactory()

        # User1 follows user2
        Follow(follower=user1, followed=user2).save()

        # Get access token for user1
        access_token = get_access_token(user1)

        # Try to block a user that is being followed
        response = self.POSTRequest(self.route.format(user2.username), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 204)

    def test_block_user_followed(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to block
        user2 = UserFactory()

        # User2 follows user1
        Follow(follower=user2, followed=user1).save()

        # Get access token for user1
        access_token = get_access_token(user1)

        # Try to block a user that is following the blocker
        response = self.POSTRequest(self.route.format(user2.username), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 204)

    def test_block_user_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get access token for the user
        access_token = get_access_token(user)

        # Try to block a nonexistent user
        response = self.POSTRequest(self.route.format('nonexistent'), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 404)

        # Assert the response message
        self.assertMessage(response, 'User not found.')

    def test_block_user_already_blocked(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to block
        user2 = UserFactory()

        # User1 blocks user2
        Block(blocker=user1, blocked=user2).save()

        # Get access token for user1
        access_token = get_access_token(user1)

        # Try to block a user that is already blocked
        response = self.POSTRequest(self.route.format(user2.username), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 400)

        # Assert the response message
        self.assertMessage(response, 'You are already blocking this user.')