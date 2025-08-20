# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.community_factory import CommunityFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.post import Post

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetAllByCommunity(BasePaginationTest):
    def test_get_all_by_community(self):
        # Create a community
        community = CommunityFactory()

        # Number of posts to create
        n = 5

        # Create a post
        PostFactory.create_batch(n, community=community)

        # Set the args
        args = {}

        # Get all posts by the community
        posts_by_community = Post.get_all_by_community(community, args)

        # Assert that posts_by_community is a Pagination object
        self.assertIsInstance(posts_by_community, Pagination)

        # Get the items
        items = posts_by_community.items

        # Assert the number of posts
        self.assertEqual(len(items), n)

    def test_get_all_by_community_empty(self):
        # Create a community
        community = CommunityFactory()

        # Set the args
        args = {}

        # Get all posts by the community
        posts_by_community = Post.get_all_by_community(community, args)

        # Assert that posts_by_community is a Pagination object
        self.assertIsInstance(posts_by_community, Pagination)

        # Get the items
        items = posts_by_community.items

        # Assert that posts_by_community is an empty list
        self.assertEqual(len(items), 0)
