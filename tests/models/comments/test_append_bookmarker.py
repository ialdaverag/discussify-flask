# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory


class TestAppendBookmarker(BaseTestCase):
    def test_append_bookmarker(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the comment's bookmarkers
        comment.append_bookmarker(user)

        # Assert that the user is in the comment's bookmarkers
        self.assertIn(user, comment.comment_bookmarkers)
