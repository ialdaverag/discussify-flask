#  base
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory


class TestRemoveModerator(BaseTestCase):
    def test_remove_moderator(self):
        moderator = UserFactory()

        community = CommunityFactory()
        community.append_moderator(moderator)

        self.assertIn(moderator, community.moderators)
        
        community.remove_moderator(moderator)
        
        self.assertNotIn(moderator, community.moderators)
        
        self.assertEqual(community.stats.moderators_count, 0)