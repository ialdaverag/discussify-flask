# tests
from tests.base.base_pagination_test import BasePaginationTest

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory


class TestReadComments(BasePaginationTest):
    route = '/user/{}/comments'

    def test_read_comments(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        CommentFactory.create_batch(n, owner=user)

        # Get user comments
        response = self.GETRequest(self.route.format(user.username))

        # Assert standard pagination response for comments
        self.assert_standard_pagination_response(response, expected_total=n, data_key='comments')

    def test_read_comments_args(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        CommentFactory.create_batch(n, owner=user)

        # Get user comments with pagination
        response = self.GETRequest(self.route.format(user.username), query_string={'page': 1, 'per_page': 5})

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=5,
            expected_total=n,
            data_key='comments'
        )

    def test_read_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Get the user comments
        response = self.GETRequest(self.route.format(user.username))

        # Assert standard pagination response with 0 total
        self.assert_standard_pagination_response(response, expected_total=0, data_key='comments')

    def test_read_comments_empty_args(self):
        # Create a user
        user = UserFactory()

        # Get the user comments with pagination
        response = self.GETRequest(self.route.format(user.username), query_string={'page': 1, 'per_page': 5})

        # Assert paginated response with 0 total
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=5,
            expected_total=0,
            data_key='comments'
        )

    def test_read_comments_nonexistent_user(self):
        # Try to get comments of a nonexistent user
        response = self.GETRequest(self.route.format('nonexistent'))

        # Assert that the response status code is 404
        self.assertStatusCode(response, 404)

        # Get response data
        data = response.json

        # Assert that the error message is 'User not found.'
        self.assertEqual(data['message'], 'User not found.')
