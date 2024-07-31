#  base
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory


class TestAppendModerator(BaseTestCase):
    def test_append_moderator(self):
        community = CommunityFactory()
        
        moderator = UserFactory()

        community.append_moderator(moderator)
        
        self.assertIn(moderator, community.moderators)
        self.assertEqual(community.stats.moderators_count, 1)