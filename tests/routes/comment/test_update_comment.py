# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory

# Utils
from tests.utils.tokens import get_access_token


class TestUpdateComment(BaseTestCase):
    route = '/comment/{}'

    def test_update_comment(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        owner = comment.owner
        
        # Get the access token
        access_token = get_access_token(owner)
        
        # Data to be sent
        json = {
            'content': 'Comment updated.',
        }

        # Update the comment
        response = self.client.patch(
            self.route.format(comment.id), 
            json=json,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(200, response.status_code)

    def test_update_comment_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)
        
        # Data to be sent
        json = {
            'content': 'Comment updated.',
        }

        # Update the comment
        response = self.client.patch(
            self.route.format(404), 
            json=json,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(404, response.status_code)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Comment not found.')

    def test_update_comment_missing_content(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        owner = comment.owner
        
        # Get the access token
        access_token = get_access_token(owner)
        
        # Data to be sent
        json = {}

        # Update the comment
        response = self.client.patch(
            self.route.format(comment.id), 
            json=json,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(400, response.status_code)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIn('errors', data)

        # Get errors from the response data
        errors = data['errors']

        # Assert keys in errors
        self.assertIn('content', errors)

        # Assert errors values
        self.assertEqual(errors['content'], ['Missing data for required field.'])


    def test_update_comment_being_banned(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        owner = comment.owner
    
        # Append the owner to the post's community banned list
        comment.post.community.append_banned(owner)

        # Get the access token
        access_token = get_access_token(owner)
        
        # Data to be sent
        json = {
            'content': 'Comment updated.',
        }

        # Update the comment
        response = self.client.patch(
            self.route.format(comment.id), 
            json=json,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(400, response.status_code)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are banned from this community.')
