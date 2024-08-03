# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_vote_factory import PostVoteFactory
from tests.factories.post_factory import PostFactory

# Utils
from tests.utils.tokens import get_access_token


class TestReadPostUpvoters(BaseTestCase):
    route = '/post/{}/upvoters'

    def test_read_post_upvoters(self):
        # Create a post
        post = PostFactory()

        # Create some upvoters
        PostVoteFactory.create_batch(5, post=post, direction=1)

        # Get the upvoters
        response = self.client.get(
            self.route.format(post.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert the number of upvoters
        self.assertEqual(len(data), 5)

    def test_read_post_upvoters_empty(self):
        # Create a post
        post = PostFactory()

        # Get the upvoters
        response = self.client.get(
            self.route.format(post.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert the number of upvoters
        self.assertEqual(len(data), 0)

    def test_read_post_upvoters_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Get the upvoters
        response = self.client.get(
            self.route.format(404),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 404)
