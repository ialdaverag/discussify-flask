# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from app.models.user import Block
from app.models.user import Follow

# Utils
from tests.utils.assert_pagination import assert_pagination_structure
from tests.utils.assert_list import assert_user_list
from tests.utils.tokens import get_access_token


class BasePaginationTest(BaseTestCase):
    def assert_pagination_response(
            self, 
            response, 
            expected_page, 
            expected_pages, 
            expected_per_page, 
            expected_total, 
            expected_users
        ):
        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the JSON response
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure(
            self, 
            pagination,  
            expected_page=expected_page,
            expected_pages=expected_pages,
            expected_per_page=expected_per_page,
            expected_total=expected_total,
        )

        # Get the data from the pagination
        data = pagination['users']

        # Assert the user list
        assert_user_list(self, data, expected_users)

    def setup_users(self, count):
        # Create users
        users = UserFactory.create_batch(count)

        return users

    def setup_authenticated_user(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        return user, access_token

    def block_users(self, blocker, blocked, users, count):
        # Block users
        for _ in users[:count]:
            Block(blocker=blocker, blocked=blocked).save()

    def follow_users(self, follower, followed, users, count):
        # Follow users
        for _ in users[:count]:
            Follow(follower=follower, followed=followed).save()
    
