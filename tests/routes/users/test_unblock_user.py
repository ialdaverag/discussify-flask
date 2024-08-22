# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow
from app.models.user import Block

# Utils
from tests.utils.tokens import get_access_token


class TestUnblockUser(BaseTestCase):
    route = '/user/{}/unblock'

    def test_unblock_user(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to block
        user2 = UserFactory()

        # User1 blocks user2
        Block(blocker=user1, blocked=user2).save()

        # Get access token for user1
        access_token = get_access_token(user1)

        # User1 unblocks user2
        response = self.client.post(
            self.route.format(user2.username), 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 204
        self.assertEqual(response.status_code, 204)

    def test_unblock_user_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get access token for the user
        access_token = get_access_token(user)

        # Try to unblock a nonexistent user
        response = self.client.post(
            self.route.format('inexistent'), 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert user data structure
        self.assertIn('message', data)

        # Assert the error message
        self.assertEqual(data['message'], 'User not found.')

    def test_unblock_user_not_blocked(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to block
        user2 = UserFactory()

        # Get access token for user1
        access_token = get_access_token(user1)

        # Try to unblock a user that is not blocked
        response = self.client.post(
            self.route.format(user2.username), 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status
        self.assertEqual(response.status_code, 400)

        # Get response data
        data = response.json

        # Assert user data structure
        self.assertIn('message', data)

        # Assert the error message
        self.assertEqual(data['message'], 'You are not blocking this user.')