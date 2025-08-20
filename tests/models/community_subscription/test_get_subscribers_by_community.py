# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunitySubscriber

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetSubscribersByCommunity(BasePaginationTest):
    def test_get_subscribers_by_community(self):
        # Number of users to create
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create a list of users
        users = UserFactory.create_batch(n)

        # Subscribe the users to the community
        for user in users:
            CommunitySubscriber(community=community, user=user).save()

        # Set args
        args = {}

        # Get the subscribers
        subscribers = CommunitySubscriber.get_subscribers_by_community(community, args)

        # Assert that subscribers is a Pagination object
        self.assertIsInstance(subscribers, Pagination)

        # Get the items
        subscribers_items = subscribers.items

        # Assert that subscribers is a list
        self.assertIsInstance(subscribers_items, list)

        # Assert the number of subscribers
        self.assertEqual(len(subscribers_items), n)

    def test_get_subscribers_by_community_empty(self):
        # Create a community
        community = CommunityFactory()

        # Set args
        args = {}

        # Get the subscribers
        subscribers = CommunitySubscriber.get_subscribers_by_community(community, args)

         # Assert that subscribers is a Pagination object
        self.assertIsInstance(subscribers, Pagination)

        # Get the items
        subscribers_items = subscribers.items

        # Assert that subscribers is a list
        self.assertIsInstance(subscribers_items, list)

        # Assert that the subscribers is an empty list
        self.assertEqual(subscribers_items, [])