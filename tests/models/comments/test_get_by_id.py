# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.comment_factory import CommentFactory

# Models
from app.models.comment import Comment

# Errors
from app.errors.errors import NotFoundError


class TestGetById(BaseTestCase):
    def test_get_by_id(self):
        # Create a comment 
        comment_to_find = CommentFactory()

        # Get the comment by id
        comment = Comment.get_by_id(comment_to_find.id)

        # Assert that the comment is the one we are looking for
        self.assertEqual(comment.id, comment_to_find.id)

    def test_get_by_id__nonexistent(self):
        # Attempt to get a comment that does not exist
        with self.assertRaises(NotFoundError):
            Comment.get_by_id(1)
