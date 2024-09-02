# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_vote_factory import PostVoteFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.user import Block

# Utils
from tests.utils.tokens import get_access_token
from tests.utils.assert_pagination import assert_pagination_structure
from tests.utils.assert_list import assert_user_list


class TestReadPostDownvoters(BaseTestCase):
    route = '/post/{}/downvoters'

    def test_read_post_downvoters(self):
        # Number of downvoters
        n = 5

        # Create a post
        post = PostFactory()

        # Create some downvoters
        PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
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
        users = pagination.get('users')

        # Assert the response data structure
        assert_user_list(self, users, n)

    def test_read_post_downvoters_args(self):
        # Number of downvoters
        n = 5

        # Create a post
        post = PostFactory()

        # Create some downvoters
        PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id),
            query_string={'page': 1, 'per_page': 5}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
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
        users = pagination.get('users')

        # Assert the response data structure
        assert_user_list(self, users, n)

    def test_read_post_downvoters_authenticated(self):
        # Number of downvoters
        n = 5

        # Create a post
        post = PostFactory()

        # Create some downvoters
        PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
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
        users = pagination.get('users')

        # Assert the response data structure
        assert_user_list(self, users, n)

    def test_read_post_downvoters_authenticated_args(self):
        # Number of downvoters
        n = 5

        # Create a post
        post = PostFactory()

        # Create some downvoters
        PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id),
            query_string={'page': 1, 'per_page': 5}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
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
        users = pagination.get('users')

        # Assert the response data structure
        assert_user_list(self, users, n)

    def test_read_post_downvoters_with_blocked(self):
        # Number of downvoters
        n = 5

        # Number of blocked downvoters
        b = 2

        # Create a post
        post = PostFactory()

        # Create some downvoters
        downvoters = PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Create a user
        user = UserFactory()

        # Block the downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=user, blocked=downvoter.user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
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
        users = pagination.get('users')

        # Assert the response data structure
        assert_user_list(self, users, n - b)

    def test_read_post_downvoters_with_blockers_args(self):
        # Number of downvoters
        n = 5

        # Number of blockers
        b = 3

        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Create some downvoters
        downvoters = PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Block the user from the first 3 downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=downvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'},
            query_string={'page': 1, 'per_page': 5}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
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
        users = pagination.get('users')

        # Assert the response data structure
        assert_user_list(self, users, n - b)

    def test_read_post_downvoters_with_blockers(self):
        # Number of downvoters
        n = 5

        # Number of blockers
        b = 3

        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Create some downvoters
        downvoters = PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Block the user from the first 3 downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=downvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
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
        users = pagination.get('users')

        # Assert the response data structure
        assert_user_list(self, users, n - b)

    def test_read_post_downvoters_with_blockers_args(self):
        # Number of downvoters
        n = 5

        # Number of blockers
        b = 3

        # Create a user
        user = UserFactory()

        # Create a post
        post = PostFactory()

        # Create some downvoters
        downvoters = PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Block the user from the first 3 downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=downvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'},
            query_string={'page': 1, 'per_page': 5}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
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
        users = pagination.get('users')

        # Assert the response data structure
        assert_user_list(self, users, n - b)

    def test_read_post_downvoters_with_blocked_and_blockers(self):
        # Number of downvoters
        n = 5

        # Number of blocked downvoters
        b = 2

        # Number of blockers
        c = 2

        # Create a post
        post = PostFactory()

        # Create some downvoters
        downvoters = PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Create a user
        user = UserFactory()

        # Block the downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=user, blocked=downvoter.user).save()

        # Block the user
        for downvoter in downvoters[-c:]:
            Block(blocker=downvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b - c
        )

        # Get the users
        users = pagination.get('users')

        # Assert the response data structure
        assert_user_list(self, users, n - b - c)

    def test_read_post_downvoters_with_blocked_and_blockers_args(self):
        # Number of downvoters
        n = 5

        # Number of blocked downvoters
        b = 2

        # Number of blockers
        c = 2

        # Create a post
        post = PostFactory()

        # Create some downvoters
        downvoters = PostVoteFactory.create_batch(n, post=post, direction=-1)

        # Create a user
        user = UserFactory()

        # Block the downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=user, blocked=downvoter.user).save()

        # Block the user
        for downvoter in downvoters[-c:]:
            Block(blocker=downvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'},
            query_string={'page': 1, 'per_page': 5}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n - b - c
        )

        # Get the users
        users = pagination.get('users')

        # Assert the response data structure
        assert_user_list(self, users, n - b - c)

    def test_read_post_downvoters_empty(self):
        # Create a post
        post = PostFactory()

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
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

        # Get the users
        users = pagination.get('users')

        # Assert the response data structure
        assert_user_list(self, users, 0)

    def test_read_post_downvoters_empty_args(self):
        # Create a post
        post = PostFactory()

        # Get the downvoters
        response = self.client.get(
            self.route.format(post.id),
            query_string={'page': 1, 'per_page': 5}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=5,
            expected_total=0
        )

        # Get the users
        users = pagination.get('users')

        # Assert the response data structure
        assert_user_list(self, users, 0)

    def test_read_post_downvoters_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the downvoters
        response = self.client.get(self.route.format(404))

        # Check status code
        self.assertEqual(response.status_code, 404)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Post not found.')
