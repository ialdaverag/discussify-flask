# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory


class TestReadPosts(BaseTestCase):
    route = '/user/{}/posts'

    def test_read_posts(self):
        # Create a user
        user = UserFactory()

        # Create some posts
        PostFactory.create_batch(5, owner=user)

        # Get user posts
        response = self.client.get(self.route.format(user.username))

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the response data
        self.assertIsInstance(data, list)

    def test_read_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Get the user posts
        response = self.client.get(self.route.format(user.username))

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the response data
        self.assertEqual(data, [])

    def test_read_posts_nonexistent_user(self):
        # Try to get posts of a nonexistent user
        response = self.client.get(self.route.format('inexistent'))

        # Assert that the response status code is 404
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert user data structure
        self.assertIn('message', data)

        # Assert the error message
        self.assertEqual(data['message'], 'User not found.')
