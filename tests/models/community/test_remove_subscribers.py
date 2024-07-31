#  base
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory


class TestRemoveSubscribers(BaseTestCase):
    def test_remove_subscriber(self):
        subscriber = UserFactory()

        community = CommunityFactory()
        community.append_subscriber(subscriber)

        self.assertIn(subscriber, community.subscribers)
        
        community.remove_subscriber(subscriber)
        
        self.assertNotIn(subscriber, community.subscribers)
        
        self.assertEqual(community.stats.subscribers_count, 0)
