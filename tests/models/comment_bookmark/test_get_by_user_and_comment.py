# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory
from tests.factories.comment_bookmark_factory import CommentBookmarkFactory

# Models
from app.models.comment import CommentBookmark


class TestGetByUserAndComment(BaseTestCase):
    def test_get_by_user_and_comment(self):
        # Create a comment bookmark
        bookmark = CommentBookmarkFactory()

        # Get the user the comment bookmark
        user = bookmark.user

        # Get the comment from the comment bookmark
        comment = bookmark.comment

        # Get the comment bookmark by user and comment
        bookmark = CommentBookmark.get_by_user_and_comment(user, comment)

        # Assert the comment bookmark
        self.assertIsNotNone(bookmark)

    def test_get_by_user_and_comment_none(self):
        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Get the comment bookmark by user and comment
        bookmark = CommentBookmark.get_by_user_and_comment(user, comment)

        # Assert the comment bookmark
        self.assertIsNone(bookmark)
