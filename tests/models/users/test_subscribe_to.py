# Factories
from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Errors
from app.errors.errors import BanError
from app.errors.errors import SubscriptionError

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityBan


class TestSubscribeTo(BaseTestCase):
    def test_subscribe_to(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Subscribe to the community
        user.subscribe_to(community)

        # Check that the user is in the community subscribers
        self.assertIsNotNone(CommunitySubscriber.get_by_user_and_community(user, community))

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

        # Append the user to the community banned users
        CommunityBan(community=community, user=user).save()
        
        # Attempt to subscribe to the community
        with self.assertRaises(BanError):
            user.subscribe_to(community)