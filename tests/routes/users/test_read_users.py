# tests
from tests.base.base_pagination_test import BasePaginationTest

# factories
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadUsers(BasePaginationTest):
    route = '/user/'

    def test_read_users(self):
        # Number of users
        n = 10

        # Create multiple users using batch
        UserFactory.create_batch(n)

        # Get the users
        response = self.GETRequest(self.route)

        # Assert standard pagination response (page 1, 10 per page)
        self.assert_standard_pagination_response(response, expected_total=n, data_key='users')

    def test_read_users_with_args(self):
        # Number of users
        n = 15

        # Create multiple users using batch
        UserFactory.create_batch(n)

        # Get the users with pagination arguments
        response = self.GETRequest(
            self.route,
            query_string={'page': 2, 'per_page': 5}
        )

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=2, 
            per_page=5, 
            expected_total=n, 
            data_key='users'
        )

    def test_read_users_authenticated(self):
        # Number of users
        n = 5

        # Create a user and get users (including authenticated user)
        user, access_token = self.setup_authenticated_user()
        UserFactory.create_batch(n)

        # Get the users
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response (n + 1 for the authenticated user)
        self.assert_standard_pagination_response(response, expected_total=n + 1, data_key='users')



    def test_read_users_authenticated_with_args(self):
        # Number of users
        n = 15

        # Create a user and get users (including authenticated user)  
        user, access_token = self.setup_authenticated_user()
        UserFactory.create_batch(n)

        # Get the users with pagination arguments
        response = self.GETRequest(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert paginated response (n + 1 for the authenticated user)
        self.assert_paginated_response(
            response=response,
            page=2, 
            per_page=5, 
            expected_total=n + 1, 
            data_key='users'
        )


    def test_read_users_with_blocked(self):
        # Number of users
        n = 5
        # Number of blocked users
        b = 2

        # Create a user and additional users
        user, access_token = self.setup_authenticated_user()
        users = UserFactory.create_batch(n)

        # Block some users using helper method
        self.create_user_blocks(user, users[:b])

        # Get the users
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response (total users - blocked + authenticated user)
        self.assert_standard_pagination_response(response, expected_total=n - b + 1, data_key='users')

    def test_read_users_with_blocked_args(self):
        # Number of users
        n = 15
        # Number of blocked users
        b = 3

        # Create a user and additional users
        user, access_token = self.setup_authenticated_user()
        users = UserFactory.create_batch(n)

        # Block some users using helper method
        self.create_user_blocks(user, users[:b])

        # Get the users with pagination arguments
        response = self.GETRequest(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert paginated response (total users - blocked + authenticated user)
        self.assert_paginated_response(
            response=response,
            page=2, 
            per_page=5, 
            expected_total=n - b + 1, 
            data_key='users'
        )

    def test_read_users_with_blockers(self):
        # Number of users
        n = 5
        # Number of blockers users
        b = 3

        # Create a user and additional users
        user, access_token = self.setup_authenticated_user()
        users = UserFactory.create_batch(n)

        # Block the user (make other users block this user)
        self.create_user_blockers(user, users[:b])

        # Get the users
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response (total users - blockers + authenticated user)
        self.assert_standard_pagination_response(response, expected_total=n - b + 1, data_key='users')

    def test_read_users_with_blockers_args(self):
        # Number of users
        n = 15
        # Number of blockers users
        b = 3

        # Create a user and additional users
        user, access_token = self.setup_authenticated_user()
        users = UserFactory.create_batch(n)

        # Block the user (make other users block this user)
        self.create_user_blockers(user, users[:b])

        # Get the users with pagination arguments
        response = self.GETRequest(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert paginated response (total users - blockers + authenticated user)
        self.assert_paginated_response(
            response=response,
            page=2, 
            per_page=5, 
            expected_total=n - b + 1, 
            data_key='users'
        )

    def test_read_users_with_blocked_and_blockers(self):
        # Number of users
        n = 5
        # Number of blocked users
        b = 1
        # Number of blockers users
        c = 1

        # Create a user and additional users
        user, access_token = self.setup_authenticated_user()
        users = UserFactory.create_batch(n)

        # Block some users and have others block this user
        self.create_user_blocks(user, users[:b])
        self.create_user_blockers(user, users[b:b + c])

        # Get the users
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response (total users - blocked - blockers + authenticated user)
        self.assert_standard_pagination_response(response, expected_total=n - b - c + 1, data_key='users')

    def test_read_users_with_blocked_and_blockers_args(self):
        # Number of users
        n = 15
        # Number of blocked users
        b = 2
        # Number of blockers users
        c = 2

        # Create a user and additional users
        user, access_token = self.setup_authenticated_user()
        users = UserFactory.create_batch(n)

        # Block some users and have others block this user
        self.create_user_blocks(user, users[:b])
        self.create_user_blockers(user, users[b:b + c])

        # Get the users with pagination arguments
        response = self.GETRequest(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert paginated response (total users - blocked - blockers + authenticated user)
        self.assert_paginated_response(
            response=response,
            page=2, 
            per_page=5, 
            expected_total=n - b - c + 1, 
            data_key='users'
        )

    def test_read_users_empty(self):
        # Get the users (no users created)
        response = self.GETRequest(self.route)

        # Assert standard pagination response with 0 total
        self.assert_standard_pagination_response(response, expected_total=0, data_key='users')

    def test_read_users_empty_with_args(self):
        # Get the users with pagination arguments (no users created)
        response = self.GETRequest(
            self.route,
            query_string={'page': 2, 'per_page': 5}
        )

        # Assert paginated response with 0 total
        self.assert_paginated_response(
            response=response,
            page=2, 
            per_page=5, 
            expected_total=0, 
            data_key='users'
        )