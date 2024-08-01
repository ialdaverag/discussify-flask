# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Errors
from app.errors.errors import BanError
from app.errors.errors import SubscriptionError
from app.errors.errors import OwnershipError


class TestAppointModeratorTo(BaseTestCase):
    def test_appoint_moderator(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community subscribers
        community.append_subscriber(user)

        # Gwt the owner of the community
        owner = community.owner

        # Appoint the user as a moderator
        owner.appoint_moderator(user, community)

        # Check that the user is in the community moderators
        self.assertIn(user, community.moderators)

    def test_appoint_moderator_not_being_owner(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user1 = UserFactory()

        # Create another user
        user2 = UserFactory()

        # Append the user to the community subscribers
        community.append_subscriber(user2)

        # Attempt to appoint the user as a moderator
        with self.assertRaises(OwnershipError):
            user1.appoint_moderator(user2, community)

    def test_appoint_moderator_banned_user(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community banned users
        community.append_banned(user)

        # Get the owner of the community
        owner = community.owner

        # Attempt to appoint the user as a moderator
        with self.assertRaises(BanError):
            owner.appoint_moderator(user, community)

    def test_appoint_moderator_user_not_subscribed(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Get the owner of the community
        owner = community.owner

        # Attempt to appoint the user as a moderator
        with self.assertRaises(SubscriptionError):
            owner.appoint_moderator(user, community)

    def test_appoint_moderator_user_already_moderator(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Appoint the user as a moderator
        community.append_moderator(user)

        # Attempt to appoint the user as a moderator again
        with self.assertRaises(OwnershipError):
            user.appoint_moderator(user, community)
