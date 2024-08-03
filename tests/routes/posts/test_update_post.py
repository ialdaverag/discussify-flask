# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory
from tests.factories.post_factory import PostFactory

# Utils
from tests.utils.tokens import get_access_token


class TestUpdatePost(BaseTestCase):
    route = '/post/{}'

    def test_update_post(self):
        # Create a post
        post = PostFactory()

        # Get the owner of the post
        owner = post.owner

        # Data to be sent
        json = {
            'title': 'New title',
            'content': 'New content',
        }

        # Get the access token
        access_token = get_access_token(owner)

        # Update the post
        response = self.client.patch(
            self.route.format(post.id),
            json=json,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert keys in data
        self.assertIn('title', data)
        self.assertIn('content', data)

        # Assert that the community data is correct
        self.assertEqual(data['title'], json['title'])
        self.assertEqual(data['content'], json['content'])

    def test_update_post_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Data to be sent
        json = {
            'title': 'New title',
            'content': 'New content',
            'community_id': 1
        }

        # Get the access token
        access_token = get_access_token(user)

        # Update the post
        response = self.client.patch(
            self.route.format(404),
            json=json,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert status code
        self.assertEqual(response.status_code, 404)

        # Get the response data
        data = response.json

        # Assert keys in response data
        self.assertIn('message', data)

        # Assert response data values
        self.assertEqual(data['message'], 'Post not found.')

    def test_update_post_invalid_title(self):
        # Create a post
        post = PostFactory()

        # Get the owner of the post
        owner = post.owner

        # Data to be sent
        json = {
            'title': 'a',
            'content': 'New content',
        }

        # Get the access token
        access_token = get_access_token(owner)

        # Update the post
        response = self.client.patch(
            self.route.format(post.id),
            json=json,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

       # Get the data
        data = response.json

        # Get errors from the response data
        errors = data['errors']

        # Assert keys in errors
        self.assertIn('title', errors)

        # Assert errors values
        self.assertEqual(errors['title'], ['Title must be between 8 and 40 characters.'])


    def test_update_post_invalid_content(self):
        # Create a post
        post = PostFactory()

        # Get the owner of the post
        owner = post.owner

        # Data to be sent
        json = {
            'title': 'New title',
            'content': '',
        }

        # Get the access token
        access_token = get_access_token(owner)

        # Update the post
        response = self.client.patch(
            self.route.format(post.id),
            json=json,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

       # Get the data
        data = response.json

        # Get errors from the response data
        errors = data['errors']

        # Assert keys in errors
        self.assertIn('content', errors)

        # Assert errors values
        self.assertEqual(errors['content'], ['Content must contain at least 1 character.'])

    def test_update_post_not_being_owner(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Data to be sent
        json = {
            'community_id': post.community.id,
            'title': 'New title',
            'content': 'New content'
        }

        # Get the access token
        access_token = get_access_token(user)

        # Update the post
        response = self.client.patch(
            self.route.format(post.id),
            json=json,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 403)

        # Get the data
        data = response.json

        # Assert keys in data
        self.assertIn('message', data)

        # Assert response data values
        self.assertEqual(data['message'], 'You are not the owner of this post.')
