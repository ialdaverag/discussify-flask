# tests
from tests.routes.test_route import TestRoute

# factories
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token
from tests.utils.assert_list import assert_user_list
from tests.utils.assert_pagination import assert_pagination_structure


class TestReadBlocked(TestRoute):
    route = '/user/blocked'

    def test_read_blocked(self):
        # Number of blocked users
        n = 5

        # create a user
        user = UserFactory()

        # Create some users to block
        users = UserFactory.create_batch(n)

        # Block all users
        for u in users:
            Block(blocker=user, blocked=u).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the blocked
        response = self.GETRequest(self.route, token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=1, 
            expected_per_page=10, 
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, expected_count=n)

    def test_read_blocked_args(self):
        # Number of blocked users
        n = 15

        # create a user
        user = UserFactory()

        # Create some users to block
        users = UserFactory.create_batch(n)

        # Block all users
        for u in users:
            Block(blocker=user, blocked=u).save()

        # Get the access token
        access_token = get_access_token(user)

        # Set args
        args = {'page': 1, 'per_page': 2}

        # Get the blocked
        response = self.GETRequest(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            query_string=args
        )

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=8,
            expected_per_page=2,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, expected_count=2)

    def test_read_blocked_empty(self):
        # create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Get the blocked
        response = self.GETRequest(self.route, token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=10,
            expected_total=0
        )

        # Get response data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, expected_count=0)

    def test_read_blocked_empty_args(self):
        # create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Get the blocked
        response = self.GETRequest(self.route, token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=10,
            expected_total=0
        )

        # Get response data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, expected_count=0)

        