# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunitySubscriber

# Managers
from app.managers.community import SubscriptionManager

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestReadSubscriptions(BaseTestCase):
    def test_read_subscriptions(self):
        # Number of communities
        n = 5

        # Create a user
        user = UserFactory()

        # Create some communities
        communities = CommunityFactory.create_batch(n)

        # Make the user subscribe to the communities
        for community in communities:
            CommunitySubscriber(user=user, community=community).save()

        # Set the args
        args = {}

        # Read user subscriptions
        subscriptions_to_read = SubscriptionManager.read_subscriptions_by_user(user, args)

        # Assert subscriptions_to_read is a Pagination object
        self.assertIsInstance(subscriptions_to_read, Pagination)

        # Get the items
        subscriptions_to_read_items = subscriptions_to_read.items

        # Assert the number of subscriptions
        self.assertEqual(len(subscriptions_to_read_items), n)

        # Assert the subscriptions are the same
        self.assertEqual(communities, subscriptions_to_read_items)

    def test_read_subscriptions_empty(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # Read user subscriptions
        subscriptions_to_read = SubscriptionManager.read_subscriptions_by_user(user, args)

        # Assert subscriptions_to_read is a Pagination object
        self.assertIsInstance(subscriptions_to_read, Pagination)

        # Get the items
        subscriptions_to_read_items = subscriptions_to_read.items

        # Assert the number of subscriptions
        self.assertEqual(len(subscriptions_to_read_items), 0)
