# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory
from tests.factories.post_factory import PostFactory

# Errors
from app.errors.errors import OwnershipError

# utils
from tests.utils.tokens import get_access_token


class TestUpdatePost(BaseTestCase):
    route = '/post/{}'

    def test_update_post(self):
        # Create a post
        post = PostFactory()

        # Get the owner of the post
        owner = post.owner

        # Data to be updated
        data = {
            'title': 'New title',
            'content': 'New content',
        }
        
        # Create a post
        post = owner.update_post(**data, post=post)

        # Assert that the post data is correct
        self.assertEqual(post.title, data['title'])
        self.assertEqual(post.content, data['content'])

    def test_update_post_not_being_owner(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Data to be sent
        json = {
            'title': 'New title',
            'content': 'New content',
        }
        
        # Create a post
        with self.assertRaises(OwnershipError):
            post = user.update_post(**json, post=post)
