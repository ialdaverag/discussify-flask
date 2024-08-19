# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Managers
from app.managers.community import SubscriptionManager

# Models
from app.models.community import CommunitySubscriber


class TestReadsubscribers(BaseTestCase):
    def test_read_subscribers(self):
         # Number of communities
        n = 5

        # Create some communities
        community = CommunityFactory()

        # Create a user
        users = UserFactory.create_batch(n)

        # Make the user subscribe to the communities
        for user in users:
            CommunitySubscriber(user=user, community=community).save()

        # Read user subscriptions
        subscriptions_to_read = SubscriptionManager.read_subscribers_by_community(community)

        # Assert the number of subscriptions
        self.assertEqual(len(subscriptions_to_read), n)

        # Assert the subscriptions are the same
        self.assertEqual(users, subscriptions_to_read)

    def test_read_subscribers_no_subscribers(self):
        # Create a community
        community = CommunityFactory()

        # Read the subscribers of the community
        subscribers = SubscriptionManager.read_subscribers_by_community(community)

        # Assert that there are no subscribers
        self.assertEqual(len(subscribers), 0)

        # Assert that the subscribers are an empty list
        self.assertEqual(subscribers, [])
