# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory


class TestBelongsTo(BaseTestCase):
    def test_belongs_to_true(self):
        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory(owner=user)

        # Assert that the user belongs to the post
        self.assertTrue(post.belongs_to(user))

    def test_belongs_to_false(self):
        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Assert that the user does not belong to the post
        self.assertFalse(post.belongs_to(user))
