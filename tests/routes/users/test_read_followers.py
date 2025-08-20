# tests
from tests.base.base_pagination_test import BasePaginationTest

# factories
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Follow, Block

# utils
from tests.utils.tokens import get_access_token


class TestReadFollowers(BasePaginationTest):
    route = '/user/{}/followers'
    route_with_args = '/user/{}/followers?page={}&per_page={}'

    def test_read_followers(self):
        # Number of followers
        n = 5

        # Create a user and followers
        user = UserFactory()
        self.create_followers(user, n)

        # Get user followers
        response = self.GETRequest(self.route.format(user.username))

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n, data_key='users')

    def test_read_followers_args(self):
        # Number of followers
        n = 5

        # Create a user and followers
        user = UserFactory()
        self.create_followers(user, n)

        # Get user followers with pagination
        response = self.GETRequest(self.route_with_args.format(user.username, 1, 5))

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=1, 
            per_page=5, 
            expected_total=n, 
            data_key='users'
        )

    def test_read_followers_authenticated(self):
        # Number of followers
        n = 5

        # Create a user and followers
        user = UserFactory()
        access_token = get_access_token(user)
        self.create_followers(user, n)

        # Get user followers
        response = self.GETRequest(
            self.route.format(user.username), 
            headers={'Authorization': access_token}
        )

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n, data_key='users')

    def test_read_followers_with_blocked(self):
        # Number of users
        n = 5
        # Number of blocked users
        b = 2
        # Number of followers
        f = 3

        # Create a user and users
        user = UserFactory()
        access_token = get_access_token(user)
        users = UserFactory.create_batch(n)

        # Make the first 3 users follow the user
        self.create_follow_relationships(users[:f], user)

        # Block the last 2 users
        self.create_user_blocks(user, users[-b:])

        # Get the users
        response = self.GETRequest(self.route.format(user.username), token=access_token)

        # Assert standard pagination response (total users - blocked)
        self.assert_standard_pagination_response(response, expected_total=n - b, data_key='users')

    def test_read_followers_empty(self):
        # Create a user (no followers)
        user = UserFactory()

        # Get the user followers
        response = self.GETRequest(self.route.format(user.username))

        # Assert standard pagination response with 0 total
        self.assert_standard_pagination_response(response, expected_total=0, data_key='users')

    def test_read_followers_nonexistent_user(self):
        # Try to get followers of a nonexistent user
        response = self.GETRequest(self.route.format('inexistent'))

        # Assert error response
        self.assertStatusCode(response, 404)
        self.assertMessage(response, 'User not found.')

    # NOTE: Additional test methods with similar patterns can be refactored following the same approach:
    # - test_read_followers_authenticated_args
    # - test_read_followers_with_blocked_args  
    # - test_read_followers_with_blockers
    # - test_read_followers_with_blockers_args
    # - test_read_followers_with_blocked_and_blockers
    # - test_read_followers_with_blocked_and_blockers_args
    # - test_read_followers_empty_args
    #
    # Each follows the pattern of:
    # 1. Setup users and relationships using helper methods
    # 2. Make request using GETRequest  
    # 3. Assert using assert_standard_pagination_response or assert_paginated_response
