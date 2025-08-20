# Tests
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory


class TestReadPosts(BasePaginationTest):
    route = '/user/{}/posts'

    def test_read_posts(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some posts
        PostFactory.create_batch(n, owner=user)

        # Get user posts
        response = self.GETRequest(self.route.format(user.username))

        # Assert standard pagination response for posts
        self.assert_standard_pagination_response(response, expected_total=n, data_key='posts')

    def test_read_posts_args(self):
        # Number of posts
        n = 15

        # Create a user
        user = UserFactory()

        # Create some posts
        PostFactory.create_batch(n, owner=user)

        # Get user posts with pagination
        response = self.GETRequest(self.route.format(user.username), 
            query_string={'page': 2, 'per_page': 5}
        )

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=2,
            per_page=5,
            expected_total=n,
            data_key='posts'
        )


    def test_read_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Get the user posts
        response = self.GETRequest(self.route.format(user.username))

        # Assert standard pagination response with 0 total
        self.assert_standard_pagination_response(response, expected_total=0, data_key='posts')

    def test_read_posts_empty_args(self):
        # Create a user
        user = UserFactory()

        # Get the user posts with pagination
        response = self.GETRequest(self.route.format(user.username),
            query_string={'page': 2, 'per_page': 5}
        )

        # Assert paginated response with 0 total
        self.assert_paginated_response(
            response=response,
            page=2,
            per_page=5,
            expected_total=0,
            data_key='posts'
        )

    def test_read_posts_nonexistent_user(self):
        # Try to get posts of a nonexistent user
        response = self.GETRequest(self.route.format('inexistent'))

        # Assert that the response status code is 404
        self.assertStatusCode(response, 404)

        # Get response data
        data = response.json

        # Assert user data structure
        self.assertIn('message', data)

        # Assert the error message
        self.assertEqual(data['message'], 'User not found.')
