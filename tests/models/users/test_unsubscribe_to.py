# Factories
from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Errors
from app.errors.errors import SubscriptionError
from app.errors.errors import OwnershipError


class TestUnsubscribeTo(BaseTestCase):
    def test_unsubscribe_to(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # 
        community.append_subscriber(user)

        # Unsubscribe to the community
        user.unsubscribe_to(community)

        # Check that the user is not in the community subscribers
        self.assertNotIn(community, user.subscriptions)

    def test_unsubscribe_to_being_not_subscribed(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Attempt to unsubscribe to the community
        with self.assertRaises(SubscriptionError):
            user.unsubscribe_to(community)

    def test_unsubscribe_to_being_the_owner(self):
        # Create a community
        community = CommunityFactory()

        # Get the owner of the community
        user = community.owner

        # Subscribe to the community
        user.subscribe_to(community)

        # Attempt to unsubscribe to the community
        with self.assertRaises(OwnershipError):
            user.unsubscribe_to(community)
