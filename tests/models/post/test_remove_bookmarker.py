# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory


class TestRemoveBookmarker(BaseTestCase):
    def test_remove_bookmarker(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the post's bookmarkers
        post.append_bookmarker(user)

        # Assert that the user is in the post's bookmarkers
        self.assertIn(user, post.bookmarkers)

        # Remove the user from the post's bookmarkers
        post.remove_bookmarker(user)

        # Assert that the user is not in the post's bookmarkers
        self.assertNotIn(user, post.bookmarkers)