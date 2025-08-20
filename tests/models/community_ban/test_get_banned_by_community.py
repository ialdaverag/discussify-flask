# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityBan

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetBannedByCommunity(BasePaginationTest):
    def test_get_banned_by_community(self):
        # Number of users to create
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create a list of users
        users = UserFactory.create_batch(n)

        # Ban the users from the community
        for user in users:
            CommunityBan(community=community, user=user).save()

        # Set args
        args = {}

        # Get the bans
        bans = CommunityBan.get_banned_by_community(community, args)

        # Assert that bans is a Pagination object
        self.assertIsInstance(bans, Pagination)

        # Get the items
        bans_items = bans.items

        # Assert that bans_items is a list
        self.assertIsInstance(bans_items, list)

        # Assert the number of bans
        self.assertEqual(len(bans_items), n)


    def test_get_banned_by_community_empty(self):
        # Create a community
        community = CommunityFactory()

        # Set args
        args = {}

        # Get the bans
        bans = CommunityBan.get_banned_by_community(community, args)

        # Assert that bans is a Pagination object
        self.assertIsInstance(bans, Pagination)

        # Get the items
        bans_items = bans.items

        # Assert that bans_items is a list
        self.assertIsInstance(bans_items, list)

        # Assert that the bans is an empty list
        self.assertEqual(bans_items, [])