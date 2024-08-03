# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory


class TestDeleteComment(BaseTestCase):
    route = '/comment/'

    def test_read_comments(self):
        # Create multiple comments
        comments = CommentFactory.create_batch(size=5)

        # Get the comments
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the number of comments
        self.assertEqual(len(data), len(comments))

        # Assert each comment
        for i, comment in enumerate(comments):
            self.assertEqual(data[i]['id'], comment.id)
            self.assertEqual(data[i]['content'], comment.content)
            self.assertEqual(data[i]['created_at'], comment.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
            self.assertEqual(data[i]['updated_at'], comment.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_read_commens_empty(self):
        # Get the comments
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the community
        self.assertEqual(len(data), 0)