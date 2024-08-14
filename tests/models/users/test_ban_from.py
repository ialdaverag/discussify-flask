# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Errors
from app.errors.errors import BanError
from app.errors.errors import UnauthorizedError

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityModerator
from app.models.community import CommunityBan


class TestBanFrom(BaseTestCase):
    def test_ban_from(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Get the owner of the community
        owner = community.owner

        # Append the owner to the community moderators
        CommunityModerator(community=community, user=owner).save()

        # Ban the user from the community
        owner.ban_from(user, community)

        # Check that the user is banned from the community
        self.assertIsNotNone(CommunitySubscriber.get_by_user_and_community(user, community))

    def test_ban_from_not_moderator(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user1 = UserFactory()

        # Create another user
        user2 = UserFactory()

        # Subscribe user2 to the community
        CommunitySubscriber(community=community, user=user2).save()

        # Attempt to ban the user from the community
        with self.assertRaises(UnauthorizedError):
            user1.ban_from(user2, community)

    def test_ban_from_banned_user(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Ban the user from the community
        CommunityBan(community=community, user=user).save()

        # Get the owner of the community
        owner = community.owner

        # Append the owner to the community moderators
        CommunityModerator(community=community, user=owner).save()

        # Attempt to ban the user from the community
        with self.assertRaises(BanError):
            owner.ban_from(user, community)