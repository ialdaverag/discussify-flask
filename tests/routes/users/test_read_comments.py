# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory

# Utils
from tests.utils.assert_pagination import assert_pagination_structure_comments
from tests.utils.assert_list import assert_comment_list


class TestReadComments(BaseTestCase):
    route = '/user/{}/comments'

    def test_read_comments(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        CommentFactory.create_batch(n, owner=user)

        # Get user comments
        response = self.client.get(self.route.format(user.username))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the comments
        comments = pagination['comments']

        # Assert that the comments list has the right length
        assert_comment_list(self, comments, n)

    def test_read_comments_args(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        CommentFactory.create_batch(n, owner=user)

        # Get user comments
        response = self.client.get(self.route.format(user.username), query_string={'page': 1, 'per_page': 5})

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n
        )

        # Get the comments
        comments = pagination['comments']

        # Assert that the comments list has the right length
        assert_comment_list(self, comments, n)

    def test_read_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Get the user comments
        response = self.client.get(self.route.format(user.username))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=10,
            expected_total=0
        )

        # Get the comments
        comments = pagination['comments']

        # Assert that the comments list is empty
        assert_comment_list(self, comments)

    def test_read_comments_empty_args(self):
        # Create a user
        user = UserFactory()

        # Get the user comments
        response = self.client.get(self.route.format(user.username), query_string={'page': 1, 'per_page': 5})

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=5,
            expected_total=0
        )

        # Get the comments
        comments = pagination['comments']

        # Assert that the comments list is empty
        assert_comment_list(self, comments)

    def test_read_comments_nonexistent_user(self):
        # Try to get comments of a nonexistent user
        response = self.client.get(self.route.format('nonexistent'))

        # Assert that the response status code is 404
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert that the error message is 'User not found.'
        self.assertEqual(data['message'], 'User not found.')
