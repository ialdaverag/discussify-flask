# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.tokens import get_access_token


class TestCreatePost(BaseTestCase):
    route = '/post/'

    def test_create_post(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Append the user to the community subscribers
        community.subscribers.append(user)

        # Get the user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'community_id': community.id,
            'title': 'New post',
            'content': 'This is a new post'
        }

        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 201)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIsInstance(data, dict)

        # Assert the response data
        self.assertIn('id', data)
        self.assertIn('title', data)
        self.assertIn('content', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

        # Assert that the community data is correct
        self.assertEqual(data['title'], json['title'])
        self.assertEqual(data['content'], json['content'])

    def test_create_post_missing_community_id(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Append the user to the community subscribers
        community.subscribers.append(user)

        # Get the user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'title': 'New post',
            'content': 'This is a new post'
        }

        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

         # Get errors from the response data
        errors = data['errors']

        # Assert keys in errors
        self.assertIn('community_id', errors)

        # Assert errors values
        self.assertEqual(errors['community_id'], ['Missing data for required field.'])

    def test_create_post_missing_title(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Append the user to the community subscribers
        community.subscribers.append(user)

        # Get the user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'community_id': community.id,
            'content': 'This is a new post'
        }

        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

         # Get errors from the response data
        errors = data['errors']

        # Assert keys in errors
        self.assertIn('title', errors)

        # Assert errors values
        self.assertEqual(errors['title'], ['Missing data for required field.'])

    def test_create_post_missing_content(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Append the user to the community subscribers
        community.subscribers.append(user)

        # Get the user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'community_id': community.id,
            'title': 'New post',
        }

        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

         # Get errors from the response data
        errors = data['errors']

        # Assert keys in errors
        self.assertIn('content', errors)

        # Assert errors values
        self.assertEqual(errors['content'], ['Missing data for required field.'])

    def test_create_post_nonexistent_community_id(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Append the user to the community subscribers
        community.subscribers.append(user)

        # Get the user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'community_id': 123456789,
            'title': 'New post',
            'content': 'This is a new post'
        }

        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

         # Assert the response data
        data = response.json

        # Assert keys in response data
        self.assertIn('message', data)

        # Assert response data values
        self.assertEqual(data['message'], 'Community not found.')

    def test_create_post_invalid_title(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Append the user to the community subscribers
        community.subscribers.append(user)

        # Get the user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'community_id': community.id,
            'title': 'Ti',
            'content': 'This is a new post'
        }

        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

         # Get errors from the response data
        errors = data['errors']

        # Assert keys in errors
        self.assertIn('title', errors)

        # Assert errors values
        self.assertEqual(errors['title'], ['Title must be between 8 and 40 characters.'])

    def test_create_post_invalid_content(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Append the user to the community subscribers
        community.subscribers.append(user)

        # Get the user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'community_id': community.id,
            'title': 'New post',
            'content': ''
        }

        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

         # Get errors from the response data
        errors = data['errors']

        # Assert keys in errors
        self.assertIn('content', errors)

        # Assert errors values
        self.assertEqual(errors['content'], ['Content must contain at least 1 character.'])

    def  test_create_post_being_not_subscribed(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Get the user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'community_id': community.id,
            'title': 'New post',
            'content': 'This is a new post'
        }

        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

        # Assert keys in response data
        self.assertIn('message', data)

        # Assert response data values
        self.assertEqual(data['message'], 'You are not subscribed to this community.')

    def test_create_post_being_banned(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Append the user to the community banned users
        community.append_banned(user)

        # Get the user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'community_id': community.id,
            'title': 'New post',
            'content': 'This is a new post'
        }

        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

        # Assert keys in response data
        self.assertIn('message', data)

        # Assert response data values
        self.assertEqual(data['message'], 'You are banned from this community.')
