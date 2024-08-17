# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityBan

# Managers
from app.managers.community import SubscriptionManager

# Errors
from app.errors.errors import SubscriptionError
from app.errors.errors import BanError


class TestCreateSubscription(BaseTestCase):
    def test_subscribe_to(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Subscribe to the community
        SubscriptionManager.create(user, community)

        # Check that the user is in the community subscribers
        self.assertIsNotNone(CommunitySubscriber.get_by_user_and_community(user, community))

    def test_subscribe_to_already_subscribed(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Subscribe to the community
        SubscriptionManager.create(user, community)

        # Attempt to subscribe to the community again
        with self.assertRaises(SubscriptionError):
            SubscriptionManager.create(user, community)

    def test_subscribe_to_being_banned(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Append the user to the community banned users
        CommunityBan(community=community, user=user).save()
        
        # Attempt to subscribe to the community
        with self.assertRaises(BanError):
            SubscriptionManager.create(user, community)
