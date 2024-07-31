#  base
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory


class TestAppendBanned(BaseTestCase):
    def test_append_banned(self):
        community = CommunityFactory()
        
        banned = UserFactory()

        community.append_banned(banned)
        
        self.assertIn(banned, community.banned)
        self.assertEqual(community.stats.banned_count, 1)
