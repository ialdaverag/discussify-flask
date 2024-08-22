# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunitySubscriber


class TestGetSubscribersByCommunity(BaseTestCase):
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

        # Get the subscribers
        subscribers = CommunitySubscriber.get_subscribers_by_community(community)

        # Assert that subscribers is a list
        self.assertIsInstance(subscribers, list)

        # Assert the number of subscribers
        self.assertEqual(len(subscribers), n)

    def test_get_subscribers_by_community_empty(self):
        # Create a community
        community = CommunityFactory()

        # Get the subscribers
        subscribers = CommunitySubscriber.get_subscribers_by_community(community)

        # Assert that subscribers is a list
        self.assertIsInstance(subscribers, list)

        # Assert that the subscribers is an empty list
        self.assertEqual(subscribers, [])