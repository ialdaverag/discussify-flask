# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityModerator

# Managers
from app.managers.community import ModerationManager

# Errors
from app.errors.errors import OwnershipError
from app.errors.errors import ModeratorError


class TestDeleteModeration(BaseTestCase):
    def test_dismiss_moderator(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Subscribe the user to the community
        CommunityModerator(community=community, user=user).save()

        # Get the owner of the community
        owner = community.owner

        # Dismiss the user as a moderator
        ModerationManager.delete(owner, community, user)

        # Check that the user is not a moderator
        self.assertNotIn(user, community.moderators)

    def test_dismiss_moderator_not_being_the_owner(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user1 = UserFactory()

        # Create another user
        user2 = UserFactory()

        # Subscribe user2 to the community
        CommunityModerator(community=community, user=user2).save()

        # Attempt to dismiss the user as a moderator
        with self.assertRaises(OwnershipError):
            ModerationManager.delete(user1, community, user2)

    def test_dismiss_moderator_being_the_owner(self):
        # Create a community
        community = CommunityFactory()

        # Get the owner of the community
        owner = community.owner

        # Attempt to dismiss the user as a moderator
        with self.assertRaises(OwnershipError):
            ModerationManager.delete(owner, community, owner)

    def test_dismiss_moderator_not_moderator(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Get the owner of the community
        owner = community.owner

        # Attempt to dismiss the user as a moderator
        with self.assertRaises(ModeratorError):
            ModerationManager.delete(owner, community, user)