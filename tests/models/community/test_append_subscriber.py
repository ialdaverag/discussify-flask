#  base
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory


class TestAppendSubscribers(BaseTestCase):
    def test_append_subscriber(self):
        community = CommunityFactory()
        
        subscriber = UserFactory()

        community.append_subscriber(subscriber)
        
        self.assertIn(subscriber, community.subscribers)
        self.assertEqual(community.stats.subscribers_count, 1)