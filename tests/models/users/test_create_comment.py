# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory
from tests.factories.comment_factory import CommentFactory

# Errors
from app.errors.errors import NameError
from app.errors.errors import SubscriptionError
from app.errors.errors import BanError


class TestCreateComment(BaseTestCase):
    def test_create_comment(self):
        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Define comment data
        data = {
            'content': 'This is a test comment'
        }

        # Append the user to the post's subscribers
        post.community.append_subscriber(user)

        # Create a comment
        comment = user.create_comment(**data, post=post)

        # Assert that the comment was created
        self.assertIsNotNone(comment)

        # Assert that the comment data is correct
        self.assertEqual(comment.content, data['content'])

        # Assert that the comment owner is the user
        self.assertEqual(comment.owner, user)

        # Assert that the comment is in the user's comments
        self.assertIn(comment, user.comments)

    def test_create_comment_being_banned(self):
        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Define comment data
        data = {
            'content': 'This is a test comment'
        }

        # Append the user to the post's banned users
        post.community.append_banned(user)

        # Attempt to create a comment
        with self.assertRaises(BanError):
            user.create_comment(**data, post=post)

    def test_create_comment_being_not_subscribed(self):
        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Define comment data
        data = {
            'content': 'This is a test comment'
        }

        # Attempt to create a comment
        with self.assertRaises(SubscriptionError):
            user.create_comment(**data, post=post)