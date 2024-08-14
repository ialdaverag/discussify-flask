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

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityBan


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
        community = post.community
        CommunitySubscriber(community=community, user=user).save()

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

        # Assert that the user's stats were updated
        self.assertEqual(user.stats.comments_count, 1)

        # Assert that the post's stats were updated
        self.assertEqual(comment.post.stats.comments_count, 1)

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
        community = post.community
        CommunityBan(community=community, user=user).save()

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