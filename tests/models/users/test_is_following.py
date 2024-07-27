from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory


class TestFollow(BaseTestCase):
    def test_follow(self):
        # Create three users
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = UserFactory()

        # Make user1 follow user2
        user1.follow(user2)

        # Test that user1 is following user2
        self.assertTrue(user1.is_following(user2))
        
        # Test that user1 is not following user3
        self.assertFalse(user1.is_following(user3))

        # Test that user2 is not following user1
        self.assertFalse(user2.is_following(user1))
