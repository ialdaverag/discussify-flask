# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Errors
from app.errors.errors import SubscriptionError
from app.errors.errors import BanError

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityBan

# Managers
from app.managers.post import PostManager


class TestCreatePost(BaseTestCase):
    def test_create_post(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Append the user to the community's subscribers
        CommunitySubscriber(community=community, user=user).save()

        # Data to be sent
        data = {
            'title': 'Test Post',
            'content': 'This is a test post.'
        }

        # Create a post
        post = PostManager.create(user, community, data)

        # Assert that the post was created
        self.assertIsNotNone(post)

        # Assert that the post data is correct
        self.assertEqual(post.title, data['title'])
        self.assertEqual(post.content, data['content'])

        # Assert that the post owner is the user
        self.assertEqual(post.owner, user)

        # Assert that the post is in the user's posts
        self.assertIn(post, user.posts)

        # Assert that the post is in the community's posts
        self.assertIn(post, community.posts)

        # Assert that the user's stats were updated
        self.assertEqual(user.stats.posts_count, 1)

    def test_create_posT_being_not_subscribed(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Data to be sent
        data = {
            'title': 'Test Post',
            'content': 'This is a test post.'
        }

        # Attempt to create a post in a community the user is not subscribed to
        with self.assertRaises(SubscriptionError):
            PostManager.create(user, community, data)

    def test_create_post_being_banned(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Append the user to the community's banned list
        CommunityBan(community=community, user=user).save()

        # Data to be sent
        data = {
            'title': 'Test Post',
            'content': 'This is a test post.'
        }

        # Attempt to create a post in a community the user is banned from
        with self.assertRaises(BanError):
            PostManager.create(user, community, data)