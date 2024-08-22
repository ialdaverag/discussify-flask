# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityBan


class TestGetBannedByCommunity(BaseTestCase):
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

        # Get the bans
        bans = CommunityBan.get_banned_by_community(community)

        # Assert that bans is a list
        self.assertIsInstance(bans, list)

        # Assert the number of bans
        self.assertEqual(len(bans), n)

    def test_get_banned_by_community_empty(self):
        # Create a community
        community = CommunityFactory()

        # Get the bans
        bans = CommunityBan.get_banned_by_community(community)

        # Assert that bans is a list
        self.assertIsInstance(bans, list)

        # Assert that the bans is an empty list
        self.assertEqual(bans, [])