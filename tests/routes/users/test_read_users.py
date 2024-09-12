# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token
from tests.utils.assert_list import assert_user_list
from tests.utils.assert_pagination import assert_pagination_structure


class TestReadUsers(BaseTestCase):
    route = '/user/'

    def test_read_users(self):
        # Number of users
        n = 10

        # Create multiple users using batch
        UserFactory.create_batch(n)

        # Get the users
        response = self.client.get(self.route)

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self, 
            pagination,  
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n,
        )

        # Get the data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n)

    def test_read_users_with_args(self):
        # Number of users
        n = 15

        # Create multiple users using batch
        UserFactory.create_batch(n)

        # Get the users
        response = self.client.get(
            self.route,
            query_string={'page': 2, 'per_page': 5}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=2,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n,
        )

        # Get the data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, 5)

    def test_read_users_authenticated(self):
        # Number of users
        n = 5

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        UserFactory.create_batch(n)

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n + 1,
        )

        # Get the data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n + 1)



    def test_read_users_authenticated_with_args(self):
        # Number of users
        n = 15

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        UserFactory.create_batch(n)

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.client.get(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=2,
            expected_pages=4,
            expected_per_page=5,
            expected_total=n + 1,
        )

        # Get the data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, 5)


    def test_read_users_with_blocked(self):
        # Number of users
        n = 5

        # Number of blocked users
        b = 2

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Block some users
        for u in users[:b]:
            Block(blocker=user, blocked=u).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b + 1,
        )

        # Get the data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b + 1)

    def test_read_users_with_blocked_args(self):
        # Number of users
        n = 15

        # Number of blockers users
        b = 3

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Block the user
        for u in users[:b]:
            Block(blocker=user, blocked=u).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.client.get(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=2,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b + 1,
        )

        # Get the data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, 5)

    def test_read_users_with_blockers(self):
        # Number of users
        n = 5

        # Number of blockers users
        b = 3

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Block the user
        for u in users[:b]:
            Block(blocker=u, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b + 1,
        )

        # Get the data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b + 1)

    def test_read_users_with_blockers_args(self):
        # Number of users
        n = 15

        # Number of blockers users
        b = 3

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Block the user
        for u in users[:b]:
            Block(blocker=u, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.client.get(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=2,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b + 1,
        )

        # Get the data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, 5)

    def test_read_users_with_blocked_and_blockers(self):
        # Number of users
        n = 5

        # Number of blocked users
        b = 1

        # Number of blockers users
        c = 1

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Block some users
        for u in users[:b]:
            Block(blocker=user, blocked=u).save()

        # Block the user
        for u in users[b:b + c]:
            Block(blocker=u, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b - c + 1,
        )

        # Get the data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b - c + 1)

    def test_read_users_with_blocked_and_blockers_args(self):
        # Number of users
        n = 15

        # Number of blocked users
        b = 2

        # Number of blockers users
        c = 2

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Block some users
        for u in users[:b]:
            Block(blocker=user, blocked=u).save()

        # Block the user
        for u in users[b:b + c]:
            Block(blocker=u, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.client.get(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=2,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b - c + 1,
        )

        # Get the data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, 5)

    def test_read_users_empty(self):
        # Get the users
        response = self.client.get(self.route)

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=10,
            expected_total=0,
        )

        # Get the data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, 0)

    def test_read_users_empty_with_args(self):
        # Get the users
        response = self.client.get(
            self.route,
            query_string={'page': 2, 'per_page': 5}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=2,
            expected_pages=0,
            expected_per_page=5,
            expected_total=0,
        )

        # Get the data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, 0)