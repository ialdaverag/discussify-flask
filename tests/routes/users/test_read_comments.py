# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory


class TestReadComments(BaseTestCase):
    route = '/user/<string:username>/comments'

    def test_read_comments(self):
        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(5, owner=user)

        # Get user comments
        response = self.client.get(f'/user/{user.username}/comments')

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

    def test_read_comments_nonexistent_user(self):
        # Try to get comments of a nonexistent user
        response = self.client.get('/user/inexistent/comments')

        # Assert that the response status code is 404
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert that the error message is 'User not found.'
        self.assertEqual(data['message'], 'User not found.')

    def test_read_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Get the user comments
        response = self.client.get(f'/user/{user.username}/comments')

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is an empty list
        self.assertEqual(data, [])