# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.community_factory import CommunityFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.post import Post


class TestGetAllByCommunity(BaseTestCase):
    def test_get_all_by_community(self):
        # Create a community
        community = CommunityFactory()

        # Number of posts to create
        n = 5

        # Create a post
        PostFactory.create_batch(n, community=community)

        # Get all posts by the community
        posts_by_community = Post.get_all_by_community(community)

        # Assert the number of posts
        self.assertEqual(len(posts_by_community), n)

    def test_get_all_by_community_empty(self):
        # Create a community
        community = CommunityFactory()

        # Get all posts by the community
        posts_by_community = Post.get_all_by_community(community)

        # Assert that posts_by_community is an empty list
        self.assertEqual(posts_by_community, [])
