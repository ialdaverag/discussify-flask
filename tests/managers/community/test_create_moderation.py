# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityModerator
from app.models.community import CommunityBan

# Managers
from app.managers.community import ModerationManager

# Errors
from app.errors.errors import SubscriptionError
from app.errors.errors import OwnershipError
from app.errors.errors import BanError
from app.errors.errors import ModeratorError


class TestCreateModeration(BaseTestCase):
    def test_make_a_user_moderator(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Gwt the owner of the community
        owner = community.owner

        # Make the user a moderator
        ModerationManager.create(owner, community, user)

        # Check that the user is in the community moderators
        self.assertIsNotNone(CommunityModerator.get_by_user_and_community(user, community))

    def test_make_a_user_moderator_not_being_owner(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user1 = UserFactory()

        # Create another user
        user2 = UserFactory()

        # Append the user to the community subscribers
        CommunitySubscriber(community=community, user=user1).save()

        # Attempt to make the user a moderator
        with self.assertRaises(OwnershipError):
            ModerationManager.create(user2, community, user1)

    def test_make_a_user_moderator_banned_user(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community banned users
        CommunityBan(community=community, user=user).save()

        # Get the owner of the community
        owner = community.owner

        # Attempt to make the user a moderator
        with self.assertRaises(BanError):
            ModerationManager.create(owner, community, user)

    def test_make_a_user_moderator_user_not_subscribed(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Get the owner of the community
        owner = community.owner

        # Attempt to make the user a moderator
        with self.assertRaises(SubscriptionError):
            ModerationManager.create(owner, community, user)

    def test_make_a_user_moderator_user_already_moderator(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Get the owner of the community
        owner = community.owner

        # Append the user to the community subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Make the user a moderator
        CommunityModerator(community=community, user=user).save()

        # Attempt to appoint the user as a moderator again
        with self.assertRaises(ModeratorError):
            ModerationManager.create(owner, community, user)