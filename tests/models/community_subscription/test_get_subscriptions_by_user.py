# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunitySubscriber


class TestGetSubscriptionsByUser(BaseTestCase):
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

        # Get the subscriptions
        subscriptions = CommunitySubscriber.get_subscriptions_by_user(user)

        # Assert that subscriptions is a list
        self.assertIsInstance(subscriptions, list)

        # Assert the number of subscriptions
        self.assertEqual(len(subscriptions), n)

    def test_get_subscriptions_by_user_empty(self):
        # Create a user
        user = UserFactory()

        # Get the subscriptions
        subscriptions = CommunitySubscriber.get_subscriptions_by_user(user)

        # Assert that subscriptions is a list
        self.assertIsInstance(subscriptions, list)

        # Assert that the subscriptions is an empty list
        self.assertEqual(subscriptions, [])