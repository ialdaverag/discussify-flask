# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityModerator


class TestGetByUserAndCommunity(BaseTestCase):
    def test_get_by_user_and_community(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Get the moderator
        moderator = CommunityModerator.get_by_user_and_community(user, community)

        # Assert the moderator
        self.assertEqual(moderator, moderator)

    def test_get_by_user_and_community_none(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Get the moderator
        moderator = CommunityModerator.get_by_user_and_community(user, community)

        # Assert that the moderator is None
        self.assertIsNone(moderator)
