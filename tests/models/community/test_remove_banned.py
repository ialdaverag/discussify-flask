# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory


class TestRemoveBan(BaseTestCase):
    def test_remove_ban(self):
        # Create a banned user
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community banned users
        community.append_banned(user)

        # Assert that the user is in the community banned users
        self.assertIn(user, community.banned)

        # Remove the user from the community banned users
        community.remove_banned(user)

        # Assert that the user is not in the community banned users
        self.assertNotIn(user, community.banned)
