#  base
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory


class TestRemoveBan(BaseTestCase):
    def test_remove_ban(self):
        banned = UserFactory()

        community = CommunityFactory()
        community.append_banned(banned)

        self.assertIn(banned, community.banned)

        community.remove_banned(banned)

        self.assertNotIn(banned, community.banned)

        self.assertEqual(community.stats.banned_count, 0)