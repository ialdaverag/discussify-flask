# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory


class TestIsBannedFrom(BaseTestCase):
    def test_is_banned_from_true(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community banned
        community.append_banned(user)

        # Check that the user is banned from the community
        self.assertTrue(user.is_banned_from(community))

    def test_is_banned_from_false(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Assert that the user is not banned from the community
        self.assertFalse(user.is_banned_from(community))