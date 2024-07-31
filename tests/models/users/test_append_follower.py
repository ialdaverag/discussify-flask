#  base
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory


class TestAppendFollower(BaseTestCase):
    def test_append_follower(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to append as a follower
        user2 = UserFactory()

        # Append user2 as a follower of user1
        user2.append_follower(user1)

        # Assert that user2 is in user1's followers
        self.assertIn(user1, user2.followers)
