# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunitySubscriber


class TestGetByUserAndCommunity(BaseTestCase):
    def test_get_by_user_and_community(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Subscribe the user to the community
        CommunitySubscriber(community=community, user=user).save()

        # Get the subscription
        subscription = CommunitySubscriber.get_by_user_and_community(user, community)

        # Assert the subscription
        self.assertEqual(subscription, subscription)

    def test_get_by_user_and_community_none(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Get the subscription
        subscription = CommunitySubscriber.get_by_user_and_community(user, community)

        # Assert that the subscription is None
        self.assertIsNone(subscription)
