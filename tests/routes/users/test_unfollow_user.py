# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Follow

# utils
from tests.utils.tokens import get_access_token


class TestUnfollowUser(BaseTestCase):
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
        response = self.client.post(
            self.route.format(user2.username), 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 204 (No Content)
        self.assertEqual(response.status_code, 204)

    def test_unfollow_user_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get access token for the user
        access_token = get_access_token(user)

        # Try to unfollow a nonexistent user
        response = self.client.post(
            self.route.format('nonexistent'), 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert user data structure
        self.assertIn('message', data)

        # Assert that the error message is 'User not found.'
        self.assertEqual(data['message'], 'User not found.')

    def test_unfollow_user_not_followed(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to follow
        user2 = UserFactory()

        # Get access token for user1
        access_token = get_access_token(user1)

        # Try to unfollow user2 without following them
        response = self.client.post(
            self.route.format(user2.username), 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

        # Get response data
        data = response.json

        # Assert user data structure
        self.assertIn('message', data)

        # Assert that the error message is 'User is not followed.'
        self.assertEqual(data['message'], 'You are not following this user.')

    def test_unfollow_user_self(self):
        # Create a user
        user = UserFactory()

        # Get access token for the user
        access_token = get_access_token(user)

        # Try to unfollow oneself
        response = self.client.post(
            self.route.format(user.username), 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

        # Get response data
        data = response.json

        # Assert user data structure
        self.assertIn('message', data)

        # Assert that the error message is 'You cannot unfollow yourself.'
        self.assertEqual(data['message'], 'You cannot unfollow yourself.')