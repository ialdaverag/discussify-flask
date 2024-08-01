# Factories
from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory


class TestIsSubscribedTo(BaseTestCase):
    def test_is_subscribed_to_true(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the community subscribers
        community.append_subscriber(user)

        # Assert that the user is subscribed to the community
        self.assertTrue(user.is_subscribed_to(community))

    def test_is_subscribed_to_false(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Assert that the user is not subscribed to the community
        self.assertFalse(user.is_subscribed_to(community))