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


class TestCreatePost(BaseTestCase):
    def test_create_post(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Append the user to the community's subscribers
        community.append_subscriber(user)

        # Data to be sent
        json = {
            'title': 'Test Post',
            'content': 'This is a test post.'
        }

        # Create a post
        post = user.create_post(**json, community=community)

        # Assert that the post was created
        self.assertIsNotNone(post)

        # Assert that the post data is correct
        self.assertEqual(post.title, json['title'])
        self.assertEqual(post.content, json['content'])

        # Assert that the post owner is the user
        self.assertEqual(post.owner, user)

        # Assert that the post is in the user's posts
        self.assertIn(post, user.posts)

        # Assert that the post is in the community's posts
        self.assertIn(post, community.posts)

    def test_create_posT_being_not_subscribed(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Data to be sent
        json = {
            'title': 'Test Post',
            'content': 'This is a test post.'
        }

        # Attempt to create a post in a community the user is not subscribed to
        with self.assertRaises(SubscriptionError):
            user.create_post(**json, community=community)

    def test_create_post_being_banned(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Append the user to the community's banned list
        community.append_banned(user)

        # Data to be sent
        json = {
            'title': 'Test Post',
            'content': 'This is a test post.'
        }

        # Attempt to create a post in a community the user is banned from
        with self.assertRaises(BanError):
            user.create_post(**json, community=community)