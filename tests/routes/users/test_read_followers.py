# tests
from tests.routes.test_route import TestRoute

# factories
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Follow
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token
from tests.utils.assert_list import assert_user_list
from tests.utils.assert_pagination import assert_pagination_structure


class TestReadFollowers(TestRoute):
    route = '/user/{}/followers'
    route_with_args = '/user/{}/followers?page={}&per_page={}'

    def test_read_followers(self):
        # Number of followers
        n = 5

        # Create a user
        user = UserFactory()

        # Create some followers
        followers = UserFactory.create_batch(n)

        # Make the followers follow the user
        for follower in followers:
            Follow(follower=follower, followed=user).save()

        # Get user followers
        response = self.GETRequest(self.route.format(user.username))

        # Assert that the response status code is 200
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
        assert_user_list(self, data, n)
    
    def test_read_followers_args(self):
        # Number of followers
        n = 5

        # Create a user
        user = UserFactory()

        # Create some followers
        followers = UserFactory.create_batch(n)

        # Make the followers follow the user
        for follower in followers:
            Follow(follower=follower, followed=user).save()

        # Get user followers
        response = self.GETRequest(self.route_with_args.format(user.username, 1, 5))

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

       # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n)

    def test_read_followers_authenticated(self):
        # Number of followers
        n = 5

        # Create a user
        user = UserFactory()

        # Create some followers
        followers = UserFactory.create_batch(n)

        # Make the followers follow the user
        for follower in followers:
            Follow(follower=follower, followed=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get user followers
        response = self.GETRequest(self.route.format(user.username), 
            headers={'Authorization': access_token}
        )

        # Assert that the response status code is 200
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
        assert_user_list(self, data, n)

    def test_read_followers_authenticated_args(self):
        # Number of followers
        n = 5

        # Create a user
        user = UserFactory()

        # Create some followers
        followers = UserFactory.create_batch(n)

        # Make the followers follow the user
        for follower in followers:
            Follow(follower=follower, followed=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get user followers
        response = self.GETRequest(
            self.route_with_args.format(user.username, 1, 5), 
            headers={'Authorization': access_token}
        )

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n)

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
            Follow(follower=u, followed=user).save()

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

        # Get the users
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
            Follow(follower=u, followed=user).save()

        # Block the last 2 users
        for u in users[-b:]:
            Block(blocker=user, blocked=u).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.GETRequest(
            self.route_with_args.format(user.username, 1, 5),
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
            expected_per_page=5,
            expected_total=n - b
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b)

    def test_read_follwoers_with_blockers(self):
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
            Follow(follower=u, followed=user).save()

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

        # Get the users
        data = pagination.get('users')

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
            Follow(follower=u, followed=user).save()

        # Block the last 2 users
        for u in users[-b:]:
            Block(blocker=u, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the users
        response = self.GETRequest(
            self.route_with_args.format(user.username, 1, 5),
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
            expected_per_page=5,
            expected_total=n - b
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b)

    def test_read_followers_with_blocked_and_blockers(self):
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
            Follow(follower=u, followed=user).save()

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

    def test_read_followers_with_blocked_and_blockers_args(self):
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
            Follow(follower=u, followed=user).save()

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

    def test_read_followers_empty(self):
        # Create a user
        user = UserFactory()

        # Get the user followers
        response = self.GETRequest(self.route.format(user.username))

        # Assert that the response status code is 200
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
        assert_user_list(self, data, 0)

    def test_read_followers_empty_args(self):
        # Create a user
        user = UserFactory()

        # Get the user followers
        response = self.GETRequest(self.route_with_args.format(user.username, 1, 10))

        # Assert that the response status code is 200
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
        assert_user_list(self, data, 0)

    def test_read_followers_nonexistent_user(self):
        # Try to get followers of a nonexistent user
        response = self.GETRequest(self.route.format('inexistent'))

        # Assert that the response status code is 404
        self.assertStatusCode(response, 404)

        # Get response data
        data = response.json

        # Assert user data structure
        self.assertIn('message', data)

        # Assert that the error message is 'User not found.'
        self.assertEqual(data['message'], 'User not found.')
