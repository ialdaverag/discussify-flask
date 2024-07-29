#  base
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory


class TestAppendFollower(BaseTestCase):
    def test_append_follower(self):
        user1 = UserFactory()
        user2 = UserFactory()

        user2.append_follower(user1)

        self.assertIn(user1, user2.followers)
        self.assertEqual(user2.stats.followers_count, 1)