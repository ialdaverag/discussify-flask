# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory
from tests.factories.post_factory import PostFactory

# Errors
from app.errors.errors import NameError
from app.errors.errors import SubscriptionError
from app.errors.errors import BanError
from app.errors.errors import OwnershipError

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityBan

# Factories
from tests.factories.comment_factory import CommentFactory

# Managers
from app.managers.comment import CommentManager


class TestUpdateComment(BaseTestCase):
    def test_update_comment(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory(post=post, owner=user)

        # Define new comment data
        data = {
            'content': 'This is a new test comment'
        }

        # Update the comment
        updated_comment = CommentManager.update(user, comment, data)

        # Assert that the comment was updated
        self.assertIsNotNone(updated_comment)

        # Assert that the comment content was updated
        self.assertEqual(updated_comment.content, data['content'])

    def test_update_comment_not_being_the_owner(self):
        # Create a user to be the creator of the comment
        comment = CommentFactory()

        # Create another user
        user = UserFactory()

        # Define new comment data
        data = {
            'content': 'This is a new test comment'
        }

        # Attempt to update the comment
        with self.assertRaises(OwnershipError):
            CommentManager.update(user, comment, data)

    def test_update_comment_banned_from_community(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory(post=post, owner=user)

        # Define new comment data
        data = {
            'content': 'This is a new test comment'
        }

        # Ban the user from the post's community
        CommunityBan(community=post.community, user=user).save()

        # Attempt to update the comment
        with self.assertRaises(BanError):
            CommentManager.update(user, comment, data)  