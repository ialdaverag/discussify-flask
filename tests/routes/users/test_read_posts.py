# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Utils
from tests.utils.assert_pagination import assert_pagination_structure_posts
from tests.utils.assert_list import assert_post_list


class TestReadPosts(BaseTestCase):
    route = '/user/{}/posts'

    def test_read_posts(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some posts
        PostFactory.create_batch(n, owner=user)

        # Get user posts
        response = self.client.get(self.route.format(user.username))

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get posts
        posts = pagination['posts']

        # Assert posts list
        assert_post_list(self, posts, n)

    def test_read_posts_args(self):
        # Number of posts
        n = 15

        # Create a user
        user = UserFactory()

        # Create some posts
        PostFactory.create_batch(n, owner=user)

        # Get user posts
        response = self.client.get(
            self.route.format(user.username), 
            query_string={'page': 2, 'per_page': 5}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=2,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n
        )

        # Get posts
        posts = pagination['posts']

        # Assert posts list
        assert_post_list(self, posts, 5)


    def test_read_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Get the user posts
        response = self.client.get(self.route.format(user.username))

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=10,
            expected_total=0
        )

        # Get posts
        posts = pagination['posts']

        # Assert posts list
        assert_post_list(self, posts)

    def test_read_posts_empty_args(self):
        # Create a user
        user = UserFactory()

        # Get the user posts
        response = self.client.get(
            self.route.format(user.username),
            query_string={'page': 2, 'per_page': 5}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=2,
            expected_pages=0,
            expected_per_page=5,
            expected_total=0
        )

        # Get posts
        posts = pagination['posts']

        # Assert posts list
        assert_post_list(self, posts)

    def test_read_posts_nonexistent_user(self):
        # Try to get posts of a nonexistent user
        response = self.client.get(self.route.format('inexistent'))

        # Assert that the response status code is 404
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert user data structure
        self.assertIn('message', data)

        # Assert the error message
        self.assertEqual(data['message'], 'User not found.')
