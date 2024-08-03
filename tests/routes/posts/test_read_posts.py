# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory
from tests.factories.post_factory import PostFactory

# Utils
from tests.utils.tokens import get_access_token


class TestDeletePost(BaseTestCase):
    route = '/post/'

    def test_read_posts(self):
        # Create multiple communities
        posts = PostFactory.create_batch(size=5)

        # Get the posts
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the number of posts
        self.assertEqual(len(data), len(posts))

        # Assert each post
        for i, post in enumerate(posts):
            self.assertEqual(data[i]['id'], post.id)
            self.assertEqual(data[i]['title'], post.title)
            self.assertEqual(data[i]['content'], post.content)
            self.assertEqual(data[i]['created_at'], post.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
            self.assertEqual(data[i]['updated_at'], post.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_read_posts_empty(self):
        # Get the posts
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the community
        self.assertEqual(len(data), 0)