# tests
from tests.base.base_pagination_test import BasePaginationTest

# factories
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Follow
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadFollowed(BasePaginationTest):
    route = '/user/{}/following'
    route_with_args = '/user/{}/following?page={}&per_page={}'

    def test_read_followed(self):
        # Number of followed users
        n = 5

        # Create a user
        user = UserFactory()

       # Create some followed users
        followed = UserFactory.create_batch(n)

        # Make the user follow the followed users
        for user_ in followed:
            Follow(follower=user, followed=user_).save()

        # Get user followed
        response = self.GETRequest(self.route.format(user.username))

        # Assert standard pagination response for users
        self.assert_standard_pagination_response(response, expected_total=n, data_key='users')

    def test_read_followed_args(self):
        # Number of followed users
        n = 5

        # Create a user
        user = UserFactory()

        # Create some followed users
        followed = UserFactory.create_batch(n)

        # Make the user follow the followed users
        for user_ in followed:
            Follow(follower=user, followed=user_).save()

        # Get user followed
        response = self.GETRequest(
            self.route_with_args.format(user.username, 1, 5)
        )

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=5,
            expected_total=n,
            data_key='users'
        )

    def test_read_followed_authenticated(self):
        # Number of followed users
        n = 5

        # Create a user
        user = UserFactory()

        # Create some followed users
        followed = UserFactory.create_batch(n)

        # Make the user follow the followed users
        for user_ in followed:
            Follow(follower=user, followed=user_).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get user followed
        response = self.GETRequest(self.route.format(user.username), token=access_token)

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n, data_key='users')

    def test_read_followed_authenticated_args(self):
        # Number of followed users
        n = 5

        # Create a user
        user = UserFactory()

        # Create some followed users
        followed = UserFactory.create_batch(n)

        # Make the user follow the followed users
        for user_ in followed:
            Follow(follower=user, followed=user_).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get user followed
        response = self.GETRequest(
            self.route_with_args.format(user.username, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=5,
            expected_total=n,
            data_key='users'
        )

    def test_read_followers_with_blocked(self):
        # Number of users
        n = 5

        # Number of blocked users
        b = 2

        # Number of followers
        f = 3

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Make the first 3 users follow the user
        for u in users[:f]:
            Follow(follower=user, followed=u).save()

        # Block the last 2 users
        for u in users[-b:]:
            Block(blocker=user, blocked=u).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.GETRequest(self.route.format(user.username), token=access_token)

        # Assert response status code
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
            expected_total=n - b
        )

        # Get response data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b)

    def test_read_followers_with_blocked_args(self):
        # Number of users
        n = 5

        # Number of blocked users
        b = 2

        # Number of followers
        f = 3

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Make the first 3 users follow the user
        for u in users[:f]:
            Follow(follower=user, followed=u).save()

        # Block the last 2 users
        for u in users[-b:]:
            Block(blocker=user, blocked=u).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.GETRequest(
            self.route_with_args.format(user.username, 1, 10),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
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
            expected_total=n - b
        )

        # Get response data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b)

    def test_read_followers_with_blockers(self):
        # Number of users
        n = 5

        # Number of blockers
        b = 2

        # Number of followers
        f = 3

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Make the first 3 users follow the user
        for u in users[:f]:
            Follow(follower=user, followed=u).save()

        # Block the last 2 users
        for u in users[-b:]:
            Block(blocker=u, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.GETRequest(self.route.format(user.username), token=access_token)

        # Assert response status code
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
            expected_total=n - b
        )

        # Get response data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b)

    def test_read_followers_with_blockers_args(self):
        # Number of users
        n = 5

        # Number of blockers
        b = 2

        # Number of followers
        f = 3

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Make the first 3 users follow the user
        for u in users[:f]:
            Follow(follower=user, followed=u).save()

        # Block the last 2 users
        for u in users[-b:]:
            Block(blocker=u, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.GETRequest(
            self.route_with_args.format(user.username, 1, 10),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
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
            expected_total=n - b
        )

        # Get response data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b)

    def test_read_followed_with_blocked_and_blockers(self):
        # Number of users
        n = 10

        # Number of blocked users
        m = 2

        # Number of blockers
        o = 2

        # Number of followers
        f = n - m - o

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Block the first 2 users
        for u in users[:m]:
            Block(blocker=user, blocked=u).save()

        # Block the last 2 users
        for u in users[-o:]:
            Block(blocker=u, blocked=user).save()

        # Make the remaining users follow the user
        for u in users[m:n-o]:
            Follow(follower=user, followed=u).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.GETRequest(self.route.format(user.username), token=access_token)

        # Assert response status code
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
            expected_total=f
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, f)

    def test_read_followed_with_blocked_and_blockers_args(self):
        # Number of users
        n = 10

        # Number of blocked users
        m = 2

        # Number of blockers
        o = 2

        # Number of followers
        f = n - m - o

        # Create a user
        user = UserFactory()

        # Create multiple users using batch
        users = UserFactory.create_batch(n)

        # Block the first 2 users
        for u in users[:m]:
            Block(blocker=user, blocked=u).save()

        # Block the last 2 users
        for u in users[-o:]:
            Block(blocker=u, blocked=user).save()

        # Make the remaining users follow the user
        for u in users[m:n-o]:
            Follow(follower=user, followed=u).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.GETRequest(
            self.route_with_args.format(user.username, 1, 10),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert response status code
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
            expected_total=f
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, f)

    def test_read_followed_empty(self):
        # Create a user
        user = UserFactory()

        # Get the user followed
        response = self.GETRequest(self.route.format(user.username))

        # Assert standard pagination response with 0 total
        self.assert_standard_pagination_response(response, expected_total=0, data_key='users')

    def test_read_followed_empty_args(self):
        # Create a user
        user = UserFactory()

        # Get the user followed
        response = self.GETRequest(
            self.route_with_args.format(user.username, 1, 10)
        )

        # Assert paginated response with 0 total
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=10,
            expected_total=0,
            data_key='users'
        )

    def test_read_followed_nonexistent_user(self):
        # Try to get followed users of a nonexistent user
        response = self.GETRequest(self.route.format('inexistent'))

        # Assert the response status code
        self.assertStatusCode(response, 404)

        # Get response data
        data = response.json

        # Assert user data structure
        self.assertIn('message', data)

        # Assert the error message
        self.assertEqual(data['message'], 'User not found.')
