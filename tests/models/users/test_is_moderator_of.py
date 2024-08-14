# Factories
from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityModerator


class TestIsModeratorOf(BaseTestCase):
    def test_is_moderator_of_true(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community moderators
        CommunityModerator(community=community, user=user).save()

        # Assert that the user is a moderator of the community
        self.assertTrue(user.is_moderator_of(community))

    def test_is_moderator_of_false(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Assert that the user is not a moderator of the community
        self.assertFalse(user.is_moderator_of(community))