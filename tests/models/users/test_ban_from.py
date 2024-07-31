# Factories
from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Errors
from app.errors.errors import BanError, SubscriptionError, ModeratorError, BanError, OwnershipError, UnauthorizedError


class TestBanFrom(BaseTestCase):
    def test_ban_from(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Subscribe the user to the community
        community.append_subscriber(user)

        # Get the owner of the community
        owner = community.owner

        community.append_moderator(owner)

        # Ban the user from the community
        owner.ban_from(user, community)

        # Check that the user is banned from the community
        self.assertIn(user, community.banned)

    def test_ban_from_not_moderator(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user1 = UserFactory()

        # Create another user
        user2 = UserFactory()

        # Subscribe user2 to the community
        community.append_subscriber(user2)

        # Attempt to ban the user from the community
        with self.assertRaises(UnauthorizedError):
            user1.ban_from(user2, community)

    def test_ban_from_banned_user(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Ban the user from the community
        community.append_banned(user)

        # Get the owner of the community
        owner = community.owner

        community.append_moderator(owner)

        # Attempt to ban the user from the community
        with self.assertRaises(BanError):
            owner.ban_from(user, community)