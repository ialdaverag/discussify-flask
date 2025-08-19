# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from app.models.user import Block

# Utils
from tests.utils.assert_pagination import assert_pagination_structure
from tests.utils.assert_list import assert_user_list
from tests.utils.tokens import get_access_token


class BasePaginationTest(BaseTestCase):
    route = '/user/'

    def assert_pagination_response(
            self, 
            response, 
            expected_page, 
            expected_pages, 
            expected_per_page, 
            expected_total, 
            expected_users,
            data_key='users'
        ):
        """Assert pagination response structure and data."""
        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the JSON response
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure(
            self, 
            pagination,  
            data_key=data_key,
            expected_page=expected_page,
            expected_pages=expected_pages,
            expected_per_page=expected_per_page,
            expected_total=expected_total,
        )

        # Get the data from the pagination
        data = pagination[data_key]

        # Assert the user list
        assert_user_list(self, data, expected_users)

    def make_authenticated_request(self, route=None, method='GET', user=None, query_string=None, **kwargs):
        """Make an authenticated request with a user token."""
        if user is None:
            user = UserFactory()
        
        access_token = get_access_token(user)
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {access_token}'
        kwargs['headers'] = headers
        
        route = route or self.route
        
        if method.upper() == 'GET':
            if query_string:
                kwargs['query_string'] = query_string
            return self.client.get(route, **kwargs)
        elif method.upper() == 'POST':
            return self.client.post(route, **kwargs)
        # Add other methods as needed
        
    def assert_standard_pagination_response(self, response, expected_total, data_key='users', expected_count=None):
        """Assert a standard pagination response (page 1, 10 per page)."""
        expected_count = expected_count or min(expected_total, 10)
        self.assert_pagination_response(
            response=response,
            expected_page=1,
            expected_pages=1 if expected_total <= 10 else ((expected_total - 1) // 10) + 1,
            expected_per_page=10,
            expected_total=expected_total,
            expected_users=expected_count,
            data_key=data_key
        )
        
    def assert_paginated_response(self, response, page, per_page, expected_total, data_key='users'):
        """Assert a paginated response with custom page and per_page values."""
        expected_pages = ((expected_total - 1) // per_page) + 1 if expected_total > 0 else 0
        expected_count = min(per_page, max(0, expected_total - (page - 1) * per_page))
        
        self.assert_pagination_response(
            response=response,
            expected_page=page,
            expected_pages=expected_pages,
            expected_per_page=per_page,
            expected_total=expected_total,
            expected_users=expected_count,
            data_key=data_key
        )

    def setup_users(self, count):
        """Create a batch of users."""
        users = UserFactory.create_batch(count)
        return users

    def setup_authenticated_user(self):
        """Create a user and return user with access token."""
        user = UserFactory()
        access_token = get_access_token(user)
        return user, access_token

    def create_user_blocks(self, blocker, blocked_users):
        """Create block relationships where blocker blocks multiple users."""
        for blocked_user in blocked_users:
            Block(blocker=blocker, blocked=blocked_user).save()
            
    def create_user_blockers(self, blocked_user, blocker_users):
        """Create block relationships where multiple users block one user."""
        for blocker in blocker_users:
            Block(blocker=blocker, blocked=blocked_user).save()

    def block_users(self, blocker, blocked, users, count):
        """Legacy method for backward compatibility."""
        for _ in users[:count]:
            Block(blocker=blocker, blocked=blocked).save()