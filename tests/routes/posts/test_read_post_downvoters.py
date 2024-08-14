# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_vote_factory import PostVoteFactory
from tests.factories.post_factory import PostFactory


class TestReadPostDownvoters(BaseTestCase):
    route = '/post/{}/downvoters'

    def test_read_post_downvoters(self):
        # Create a post
        post = PostFactory()

        # Create some downvoters
        PostVoteFactory.create_batch(5, post=post, direction=-1)

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert data is a list
        self.assertIsInstance(data, list)

        # Assert the number of downvoters
        self.assertEqual(len(data), 5)

    def test_read_post_downvoters_empty(self):
        # Create a post
        post = PostFactory()

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert the number of downvoters
        self.assertEqual(len(data), 0)

    def test_read_post_downvoters_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the downvoters
        response = self.client.get(self.route.format(404))

        # Check status code
        self.assertEqual(response.status_code, 404)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Post not found.')
