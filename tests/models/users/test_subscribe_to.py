# Factories
from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Errors
from app.errors.errors import BanError, SubscriptionError


class TestSubscribeTo(BaseTestCase):
    def test_subscribe_to(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Subscribe to the community
        user.subscribe_to(community)

        # Check that the user is subscribed to the community
        self.assertIn(community, user.subscriptions)

    def test_subscribe_to_already_subscribed(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Subscribe to the community
        user.subscribe_to(community)

        # Attempt to subscribe to the community again
        with self.assertRaises(SubscriptionError):
            user.subscribe_to(community)

    def test_subscribe_to_being_banned(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Ban the user from the community
        community.append_banned(user)

        # Attempt to subscribe to the community
        with self.assertRaises(BanError):
            user.subscribe_to(community)