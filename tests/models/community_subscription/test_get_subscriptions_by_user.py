# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunitySubscriber

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetSubscriptionsByUser(BasePaginationTest):
    def test_get_subscriptions_by_user(self):
        # Number of communities to create
        n = 5

        # Create a user
        user = UserFactory()

        # Create a list of communities
        communities = CommunityFactory.create_batch(n)

        # Subscribe the user to the communities
        for community in communities:
            CommunitySubscriber(community=community, user=user).save()

        # Set the args
        args = {}

        # Get the subscriptions
        subscriptions = CommunitySubscriber.get_subscriptions_by_user(user, args)

        # Assert subscriptions is a Pagination object
        self.assertIsInstance(subscriptions, Pagination)

        # Get the items
        subscriptions_items = subscriptions.items

        # Assert that items is a list
        self.assertIsInstance(subscriptions_items, list)

        # Assert the number of subscriptions
        self.assertEqual(len(subscriptions_items), n)

    def test_get_subscriptions_by_user_empty(self):
        # Create a user
        user = UserFactory()

        # Set the args
        args = {}

        # Get the subscriptions
        subscriptions = CommunitySubscriber.get_subscriptions_by_user(user, args)

        # Assert subscriptions is a Pagination object
        self.assertIsInstance(subscriptions, Pagination)

        # Get the items
        subscriptions_items = subscriptions.items

        # Assert that items is a list
        self.assertIsInstance(subscriptions_items, list)

        # Assert the number of subscriptions
        self.assertEqual(len(subscriptions_items), 0)