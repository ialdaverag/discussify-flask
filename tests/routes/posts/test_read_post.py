# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.post_factory import PostFactory


class TestReadPost(BaseTestCase):
    route = '/post/{}'

    def test_read_post(self):
        # Create a post
        post = PostFactory()

        # Read the post
        response = self.client.get(self.route.format(post.id))

        # Assert the status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert keys in data
        self.assertIn('id', data)
        self.assertIn('title', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

        # Assert that the post data is correct
        self.assertEqual(data['id'], post.id)
        self.assertEqual(data['title'], post.title)
        self.assertEqual(data['content'], post.content)
        self.assertEqual(data['created_at'], post.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(data['updated_at'], post.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_read_post_nonexistent(self):
        # Read the post
        response = self.client.get(self.route.format(404))

        # Assert the status code
        self.assertEqual(response.status_code, 404)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Post not found.')