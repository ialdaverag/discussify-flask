# Factories
from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Errors
from app.errors.errors import BanError, SubscriptionError, ModeratorError, BanError, OwnershipError


class TestDismissModerator(BaseException):
    def test_dismiss_moderator(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Subscribe the user to the community
        community.append_moderator(user)

        # Get the owner of the community
        owner = community.owner

        # Dismiss the user as a moderator
        owner.dismiss_moderator(user, community)

        # Check that the user is not a moderator
        self.assertNotIn(user, community.moderators)

    def test_dismiss_moderator_not_owner(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user1 = UserFactory()

        # Create another user
        user2 = UserFactory()

        # Subscribe user2 to the community
        community.append_moderator(user2)

        # Attempt to dismiss the user as a moderator
        with self.assertRaises(OwnershipError):
            user1.dismiss_moderator(user2, community)

    def test_dismiss_moderator_being_the_owner(self):
        # Create a community
        community = CommunityFactory()

        # Get the owner of the community
        user = community.owner

        # Attempt to dismiss the user as a moderator
        with self.assertRaises(ModeratorError):
            user.dismiss_moderator(user, community)

    def test_dismiss_moderator_not_moderator(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Get the owner of the community
        owner = community.owner

        # Attempt to dismiss the user as a moderator
        with self.assertRaises(ModeratorError):
            owner.dismiss_moderator(user, community)