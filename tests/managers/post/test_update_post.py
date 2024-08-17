# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Errors
from app.errors.errors import OwnershipError

# Managers
from app.managers.post import PostManager

# Factories
from tests.factories.post_factory import PostFactory


class TestUpdatePost(BaseTestCase):
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
        post = PostManager.update(owner, post, data)

        # Assert that the post data is correct
        self.assertEqual(post.title, data['title'])
        self.assertEqual(post.content, data['content'])

    def test_update_post_not_being_owner(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Data to be sent
        data = {
            'title': 'New title',
            'content': 'New content',
        }
        
        # Create a post
        with self.assertRaises(OwnershipError):
            post = PostManager.update(user, post, data)