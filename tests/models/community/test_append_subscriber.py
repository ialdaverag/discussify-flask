# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory


class TestAppendSubscribers(BaseTestCase):
    def test_append_subscriber(self):
        # Create a community
        community = CommunityFactory()
        
        # Create a user
        user= UserFactory()

        # Append the user to the community subscribers
        community.append_subscriber(user)
        
        # Assert that the user is in the community subscribers
        self.assertIn(user, community.subscribers)
