# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory
from tests.factories.comment_factory import CommentFactory
from tests.factories.post_factory import PostFactory

# Utils
from tests.utils.tokens import get_access_token


class TestCreateComment(BaseTestCase):
    route = '/comment/'

    def test_create_comment(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the post's community's subscribers
        post.community.append_subscriber(user)

        # Data to be sent
        json={
                'post_id': post.id,
                'content': 'This is a comment.'
            }
        
        # Get the access token
        access_token = get_access_token(user)

        # Create a comment
        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Check status code
        self.assertEqual(response.status_code, 201)

    def test_create_comment_nonexistent_post(self):
        # Create a user
        user = UserFactory()

        # Data to be sent
        json = {
                'post_id': 404,
                'content': 'This is a comment.'
            }

        # Get the access token
        access_token = get_access_token(user)

        # Create a comment
        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Check status code
        self.assertEqual(response.status_code, 404)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Post not found.')

    def test_create_comment_missing_post_id(self):
        # Create a user
        user = UserFactory()

        # Data to be sent
        json = {
                'content': 'This is a comment.'
            }

        # Get the access token
        access_token = get_access_token(user)

        # Create a comment
        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

        # Get errors from the response data
        errors = data['errors']

        # Assert keys in errors
        self.assertIn('post_id', errors)

        # Assert errors values
        self.assertEqual(errors['post_id'], ['Missing data for required field.'])

    def test_create_comment_missing_content(self):
        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Data to be sent
        json = {
                'post_id': post.id
            }

        # Get the access token
        access_token = get_access_token(user)

        # Create a comment
        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

         # Get errors from the response data
        errors = data['errors']

        # Assert keys in errors
        self.assertIn('content', errors)

        # Assert errors values
        self.assertEqual(errors['content'], ['Missing data for required field.'])

    def test_create_comment_invalid_content(self):
        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Data to be sent
        json = {
                'post_id': post.id,
                'content': ''
            }

        # Get the access token
        access_token = get_access_token(user)

        # Create a comment
        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

         # Get errors from the response data
        errors = data['errors']

        # Assert keys in errors
        self.assertIn('content', errors)

        # Assert errors values
        self.assertEqual(errors['content'], ['Content must contain at least 1 character.'])

    def test_create_comment_not_subscribed(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Data to be sent
        json = {
                'post_id': post.id,
                'content': 'This is a comment.'
            }

        # Get the access token
        access_token = get_access_token(user)

        # Create a comment
        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are not subscribed to this community.')

    def test_create_comment_being_banned(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Append the user to the post's community's banned
        post.community.append_banned(user)

        # Data to be sent
        json = {
                'post_id': post.id,
                'content': 'This is a comment.'
            }

        # Get the access token
        access_token = get_access_token(user)

        # Create a comment
        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are banned from this community.')