#  base
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory


class TestRemoveFollower(BaseTestCase):
    def test_remove_follower(self):
        user1 = UserFactory()
        user2 = UserFactory()

        user2.append_follower(user1)
        self.assertIn(user1, user2.followers)

        user2.remove_follower(user1)
        self.assertNotIn(user1, user2.followers)

        self.assertEqual(user2.stats.followers_count, 0)