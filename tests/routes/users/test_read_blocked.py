# tests
from tests.base.base_pagination_test import BasePaginationTest

# factories
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadBlocked(BasePaginationTest):
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

        # Assert standard pagination response for users
        self.assert_standard_pagination_response(response, expected_total=n, data_key='users')

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

        # Get the blocked with pagination
        response = self.GETRequest(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            query_string={'page': 1, 'per_page': 2}
        )

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=2,
            expected_total=n,
            data_key='users'
        )

    def test_read_blocked_empty(self):
        # create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Get the blocked
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response with 0 total
        self.assert_standard_pagination_response(response, expected_total=0, data_key='users')

    def test_read_blocked_empty_args(self):
        # create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Get the blocked
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response with 0 total
        self.assert_standard_pagination_response(response, expected_total=0, data_key='users')

        