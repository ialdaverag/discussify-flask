# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory

# utils
from tests.utils.tokens import get_access_token


class TestFollowUser(BaseTestCase):
    route = '/user/<string:username>/follow'

    def test_follow_user(self):
        # Create two users
        user1 = UserFactory()
        user2 = UserFactory()

        # Get access token for user1
        access_token = get_access_token(user1)

        # User1 follows user2
        response = self.client.post(
            f'/user/{user2.username}/follow', 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 204 (No Content)
        self.assertEqual(response.status_code, 204)

    def test_follow_user_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get access token for the user
        access_token = get_access_token(user)

        # Try to follow a nonexistent user
        response = self.client.post(
            '/user/inexistent/follow', 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert that the error message is 'User not found.'
        self.assertEqual(data['message'], 'User not found.')

    def test_follow_user_already_followed(self):
        # Create two users
        user1 = UserFactory()
        user2 = UserFactory()

        # Get access token for user1
        access_token = get_access_token(user1)

        # User1 follows user2
        user1.follow(user2)

        # Try to follow user2 again
        response = self.client.post(
            f'/user/{user2.username}/follow', 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

        # Get response data
        data = response.json

        # Assert that the error message is 'You are already following this user.'
        self.assertEqual(data['message'], 'You are already following this user.')

    def test_follow_user_self(self):
        # Create a user
        user = UserFactory()

        # Get access token for the user
        access_token = get_access_token(user)

        # Try to follow oneself
        response = self.client.post(
            f'/user/{user.username}/follow', 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

        # Get response data
        data = response.json

        # Assert that the error message is 'You cannot follow yourself.'
        self.assertEqual(data['message'], 'You cannot follow yourself.')
