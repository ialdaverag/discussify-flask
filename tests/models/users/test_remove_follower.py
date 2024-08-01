# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory


class TestRemoveFollower(BaseTestCase):
    def test_remove_follower(self):
        # Create a user
        user1 = UserFactory()

        # Create a user to append as a follower
        user2 = UserFactory()

        # Append user2 as a follower of user1
        user2.append_follower(user1)

        # Assert that user1 is in user2's following
        user2.remove_follower(user1)

        # Assert that user2 is not in user1's followers
        self.assertNotIn(user1, user2.followers)
