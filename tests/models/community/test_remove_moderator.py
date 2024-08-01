# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory


class TestRemoveModerator(BaseTestCase):
    def test_remove_moderator(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community moderators
        community.append_moderator(user)

        # Assert that the user is in the community moderators
        self.assertIn(user, community.moderators)
        
        # Remove the user from the community moderators
        community.remove_moderator(user)
        
        # Assert that the user is not in the community moderators
        self.assertNotIn(user, community.moderators)
