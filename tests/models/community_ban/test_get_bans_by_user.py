# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityBan


class TestGetBansByUser(BaseTestCase):
    def test_get_bans_by_user(self):
        # Number of communities to create
        n = 5

        # Create a user
        user = UserFactory()

        # Create a list of communities
        communities = CommunityFactory.create_batch(n)

        # Ban the user from the communities
        for community in communities:
            CommunityBan(community=community, user=user).save()

        # Get the bans
        bans = CommunityBan.get_bans_by_user(user)

        # Assert that bans is a list
        self.assertIsInstance(bans, list)

        # Assert the number of bans
        self.assertEqual(len(bans), n)

    def test_get_bans_by_user_empty(self):
        # Create a user
        user = UserFactory()

        # Get the bans
        bans = CommunityBan.get_bans_by_user(user)

        # Assert that bans is a list
        self.assertIsInstance(bans, list)

        # Assert that the bans is an empty list
        self.assertEqual(bans, [])