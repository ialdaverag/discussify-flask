# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Managers
from app.managers.community import BanManager

# Models
from app.models.community import CommunityBan

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestReadBanned(BaseTestCase):
    def test_read_banned(self):
        # Number of banned users
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create some banned users
        banned_users = UserFactory.create_batch(n)

        # Ban the users from the community
        for banned_user in banned_users:
            CommunityBan(community=community, user=banned_user).save()

        # Set the args
        args = {}

        # Read the banned users of the community
        banned_users_to_read = BanManager.read_bans_by_community(community, args)

        # Assert that banned_users_to_read is a Pagination object
        self.assertIsInstance(banned_users_to_read, Pagination)

        # Get the items
        banned_users_to_read_items = banned_users_to_read.items

        # Assert that banned_users_to_read_items is a list
        self.assertIsInstance(banned_users_to_read_items, list)

        # Assert the number of banned users
        self.assertEqual(len(banned_users_to_read_items), n)

        # Assert the banned users are the same
        self.assertEqual(banned_users, banned_users_to_read_items)

    def test_read_banned_no_banned_users(self):
        # Create a community
        community = CommunityFactory()

        # Set the args
        args = {}

        # Read the banned users of the community
        banned_users = BanManager.read_bans_by_community(community, args)

        # Assert that banned_users is a Pagination object
        self.assertIsInstance(banned_users, Pagination)

        # Get the items
        banned_users_items = banned_users.items

        # Assert that there are no banned users
        self.assertEqual(len(banned_users_items), 0)

        # Assert that the banned users are an empty list
        self.assertEqual(banned_users_items, [])