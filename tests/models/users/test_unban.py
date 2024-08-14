# Factories
from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Errors
from app.errors.errors import BanError
from app.errors.errors import UnauthorizedError

# Models
from app.models.community import CommunityModerator
from app.models.community import CommunityBan


class TestUnban(BaseTestCase):
    def test_unban(self):
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

        # Unban the user from the community
        owner.unban_from(user, community)

        # Check that the user is not banned from the community
        self.assertNotIn(user, community.banned)

    def test_unban_not_moderator(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user1 = UserFactory()

        # Create another user
        user2 = UserFactory()

        # Append the user to the community banned users
        CommunityBan(community=community, user=user2).save()

        # Attempt to unban the user from the community
        with self.assertRaises(UnauthorizedError):
            user1.unban_from(user2, community)

    def test_unban_not_banned_user(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Get the owner of the community
        owner = community.owner

        # Append the owner to the community moderators
        CommunityModerator(community=community, user=owner).save()

        # Attempt to unban the user from the community
        with self.assertRaises(BanError):
            owner.unban_from(user, community)