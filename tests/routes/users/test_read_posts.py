# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory


class TestReadPosts(BaseTestCase):
    route = '/user/{}/posts'

    def test_read_posts(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some posts
        PostFactory.create_batch(n, owner=user)

        # Get user posts
        response = self.client.get(self.route.format(user.username))

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert the response data
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for post in data:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('owner', post)
            self.assertIn('community', post)
            self.assertIn('bookmarked', post)
            self.assertIn('upvoted', post)
            self.assertIn('downvoted', post)
            self.assertIn('stats', post)
            self.assertIn('created_at', post)
            self.assertIn('updated_at', post)

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
