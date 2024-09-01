# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Managers
from app.managers.community import SubscriptionManager

# Models
from app.models.community import CommunitySubscriber

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


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

        # Set args
        args = {}

        # Read user subscriptions
        subscribers = SubscriptionManager.read_subscribers_by_community(community, args)

        # Assert that subscriptions_to_read is a Pagination object
        self.assertIsInstance(subscribers, Pagination)

        # Get the items
        subscribers_items = subscribers.items

        # Assert the number of subscriptions
        self.assertEqual(len(subscribers_items), n)

        # Assert the subscriptions are the same
        self.assertEqual(users, subscribers_items)

    def test_read_subscribers_no_subscribers(self):
        # Create a community
        community = CommunityFactory()

        # Set args
        args = {}

        # Read the subscribers of the community
        subscribers = SubscriptionManager.read_subscribers_by_community(community, args)

        # Assert that subscriptions_to_read is a Pagination object
        self.assertIsInstance(subscribers, Pagination)

        # Get the items
        subscribers_items = subscribers.items

        # Assert that there are no subscribers
        self.assertEqual(len(subscribers_items), 0)

        # Assert that the subscribers are an empty list
        self.assertEqual(subscribers_items, [])
