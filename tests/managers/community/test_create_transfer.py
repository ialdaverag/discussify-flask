# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityBan

# Managers
from app.managers.community import TransferManager

# Errors
from app.errors.errors import SubscriptionError
from app.errors.errors import BanError
from app.errors.errors import OwnershipError


class CreateTransferTest(BaseTestCase):
    def test_transfer_to(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Get the owner of the community
        owner = community.owner

        # Append the owner to the community moderators
        CommunitySubscriber(community=community, user=owner).save()

        # Transfer the community to the user
        TransferManager.create(owner, community, user)

        # Check that the user is banned from the community
        self.assertIsNotNone(CommunitySubscriber.get_by_user_and_community(user, community))

    def test_transfer_to_not_owner(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user1 = UserFactory()

        # Create another user
        user2 = UserFactory()

        # Subscribe user2 to the community
        CommunitySubscriber(community=community, user=user2).save()

        # Attempt to transfer the community to the user
        with self.assertRaises(OwnershipError):
            TransferManager.create(user1, community, user2)

    def test_transfer_to_already_owner(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        owner = community.owner

        # Attempt to transfer the community to the user
        with self.assertRaises(OwnershipError):
            TransferManager.create(owner, community, owner)

    def test_transfer_to_banned_user(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Create the owner of the community
        owner = community.owner 

        # Ban the user from the community
        CommunityBan(community=community, user=user).save()

        # Attempt to transfer the community to the user
        with self.assertRaises(BanError):
            TransferManager.create(owner, community, user)

    def test_transfer_to_not_subscribed_user(self):
        # Create a community
        community = CommunityFactory()

        # Create the owner of the community
        owner = community.owner

        # Create a user
        user = UserFactory()

        # Attempt to transfer the community to the user
        with self.assertRaises(SubscriptionError):
            TransferManager.create(owner, community, user)
