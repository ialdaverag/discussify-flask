# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory

# Models
from app.models.comment import CommentBookmark


class TestIsBookmarkedBy(BaseTestCase):
    def test_is_bookmarked_by_true(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Bookmark the comment
        CommentBookmark(user=user, comment=comment).save()

        # Assert that the comment is bookmarked by the user
        self.assertTrue(comment.is_bookmarked_by(user))

    def test_is_bookmarked_by_false(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        user = UserFactory()

        # Assert that the comment is not bookmarked by the user
        self.assertFalse(comment.is_bookmarked_by(user))