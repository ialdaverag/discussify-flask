# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# utils
from tests.utils.tokens import get_access_token


class TestReadUpvotedPosts(BaseTestCase):
    route = '/user/posts/upvoted'

    def test_read_upvoted_posts(self):
        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(5)

        # Make the user subscribe to the posts' communities
        for post in posts:
            user.subscribe_to(post.community)

        # Make the user upvote the posts
        for post in posts:
            user.downvote_post(post)

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted posts
        response = self.client.get(
            f'/user/posts/downvoted',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

    def test_read_upvoted_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user upvoted posts
        response = self.client.get(
            f'/user/posts/downvoted',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is an empty list
        self.assertEqual(data, [])