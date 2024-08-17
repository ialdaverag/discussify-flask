# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunitySubscriber

# Managers
from app.managers.community import SubscriptionManager

# Errors
from app.errors.errors import SubscriptionError
from app.errors.errors import OwnershipError


class TestDeleteSubscription(BaseTestCase):
    def test_unsubscribe_to(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Subscribe to the community
        CommunitySubscriber(community=community, user=user).save()

        # Unsubscribe to the community
        SubscriptionManager.delete(user, community)

        # Check that the user is not in the community subscribers
        self.assertNotIn(community, user.subscriptions)

    def test_unsubscribe_to_being_not_subscribed(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Attempt to unsubscribe to the community
        with self.assertRaises(SubscriptionError):
            SubscriptionManager.delete(user, community)

    def test_unsubscribe_to_being_the_owner(self):
        # Create a community
        community = CommunityFactory()

        # Get the owner of the community
        user = community.owner

        # Subscribe to the community
        CommunitySubscriber(community=community, user=user).save()

        # Attempt to unsubscribe to the community
        with self.assertRaises(OwnershipError):
            SubscriptionManager.delete(user, community)