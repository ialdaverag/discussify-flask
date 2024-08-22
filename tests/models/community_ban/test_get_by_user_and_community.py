# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityBan


class TestGetByUserAndCommunity(BaseTestCase):
    def test_get_by_user_and_community(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Ban the user from the community
        CommunityBan(community=community, user=user).save()

        # Get the ban
        ban = CommunityBan.get_by_user_and_community(user, community)

        # Assert the ban
        self.assertEqual(ban, ban)

    def test_get_by_user_and_community_none(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Get the ban
        ban = CommunityBan.get_by_user_and_community(user, community)

        # Assert that the ban is None
        self.assertIsNone(ban)