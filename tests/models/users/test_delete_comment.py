# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory

# Errors
from app.errors.errors import OwnershipError

# Models
from app.models.comment import Comment


class TestCreatecomment(BaseTestCase):
    def test_delete_comment(self):
        # Create a comment
        comment = CommentFactory()

        # Get the owner of the comment
        user = comment.owner

        # Get the comment to delete
        comment_to_delete = Comment.get_by_id(comment.id)

        # Delete the comment
        user.delete_comment(comment_to_delete)

        # Assert that the comment was deleted
        self.assertNotIn(comment, user.comments)

        # Assert that the owner's stats were updated
        comments_count = user.stats.comments_count

        self.assertEqual(comments_count, 0)

    def test_delete_comment_not_being_the_owner(self):
        # Create a user to be the creator of the comment
        comment = CommentFactory()

        # Create another user
        user = UserFactory()

        # Attempt to delete the comment
        with self.assertRaises(OwnershipError):
            user.delete_comment(comment)