# Base
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.post_factory import PostFactory
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token
from tests.utils.assert_pagination import assert_pagination_structure_posts
from tests.utils.assert_list import assert_post_list


class TestDeletePost(TestRoute):
    route = '/post/'

    def test_read_posts(self):
        # Number of posts
        n = 5

        # Create multiple communities
        PostFactory.create_batch(n)

        # Get the posts
        response = self.GETRequest(self.route)

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the response pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the response data
        posts = pagination['posts']

        # Assert the response data
        assert_post_list(self, posts, expected_count=n)

    def test_read_posts_args(self):
        # Number of posts
        n = 5

        # Create multiple communities
        PostFactory.create_batch(n)

        # Get the posts
        response = self.GETRequest(
            self.route,
            query_string={'page': 1, 'per_page': 5}
        )

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the response pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n
        )

        # Get the response data
        posts = pagination['posts']

        # Assert the response data
        assert_post_list(self, posts, expected_count=n)

    def test_read_posts_authenticated(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create multiple communities
        PostFactory.create_batch(n)

        # Get user access token
        access_token = get_access_token(user)

        # Get the posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the response data
        posts = pagination['posts']

        # Assert the response data
        assert_post_list(self, posts, expected_count=n)

    def test_read_posts_authenticated_args(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create multiple communities
        PostFactory.create_batch(n)

        # Get user access token
        access_token = get_access_token(user)

        # Get the posts
        response = self.GETRequest(
            self.route,
            query_string={'page': 1, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n
        )

        # Get the response data
        posts = pagination['posts']

        # Assert the response data
        assert_post_list(self, posts, expected_count=n)

    def test_read_posts_with_blocked(self):
        # Number of posts
        n = 5

        # Create multiple users using batch
        posts = PostFactory.create_batch(n)

        # Number of blocked users
        b = 2

        # Create a user
        user = UserFactory()

        # Block some users
        for post in posts[:b]:
            Block(blocker=user, blocked=post.owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get the response data
        data = pagination['posts']

        # Assert the response data
        assert_post_list(self, data, expected_count=n - b)

    def test_read_posts_with_blocked_args(self):
        # Number of posts
        n = 5

        # Create multiple users using batch
        posts = PostFactory.create_batch(n)

        # Number of blocked users
        b = 2

        # Create a user
        user = UserFactory()

        # Block some users
        for post in posts[:b]:
            Block(blocker=user, blocked=post.owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the posts
        response = self.GETRequest(
            self.route,
            query_string={'page': 1, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get the response data
        data = pagination['posts']

        # Assert the response data
        assert_post_list(self, data, expected_count=n - b)

    def test_read_posts_with_blockers(self):
        # Number of posts
        n = 5

        # Create multiple users using batch
        posts = PostFactory.create_batch(n)

        # Number of blocked users
        b = 2

        # Create a user
        user = UserFactory()

        # Block some users
        for post in posts[:b]:
            Block(blocker=post.owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get the response data
        data = pagination['posts']

        # Assert the response data
        assert_post_list(self, data, expected_count=n - b)

    def test_read_posts_with_blockers_args(self):
        # Number of posts
        n = 5

        # Create multiple users using batch
        posts = PostFactory.create_batch(n)

        # Number of blocked users
        b = 2

        # Create a user
        user = UserFactory()

        # Block some users
        for post in posts[:b]:
            Block(blocker=post.owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the posts
        response = self.GETRequest(
            self.route,
            query_string={'page': 1, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get the response data
        data = pagination['posts']

        # Assert the response data
        assert_post_list(self, data, expected_count=n - b)

    def test_read_posts_with_blocked_and_blockers(self):
        # Number of posts
        n = 5

        # Create multiple users using batch
        posts = PostFactory.create_batch(n)

        # Create a user
        user = UserFactory()

        # Number of blocked users
        b = 2

        # Block some users
        for post in posts[:b]:
            Block(blocker=user, blocked=post.owner).save()

        # Number of blockers
        c = 2

        # Block some users
        for post in posts[-c:]:
            Block(blocker=post.owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b - c
        )

        # Get the response data
        data = pagination['posts']

        # Assert the response data
        assert_post_list(self, data, expected_count=n - b - c)

    def test_read_posts_with_blocked_and_blockers_args(self):
        # Number of posts
        n = 5

        # Create multiple users using batch
        posts = PostFactory.create_batch(n)

        # Create a user
        user = UserFactory()

        # Number of blocked users
        b = 2

        # Block some users
        for post in posts[:b]:
            Block(blocker=user, blocked=post.owner).save()

        # Number of blockers
        c = 2

        # Block some users
        for post in posts[-c:]:
            Block(blocker=post.owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the posts
        response = self.GETRequest(
            self.route,
            query_string={'page': 1, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n - b - c
        )

        # Get the response data
        data = pagination['posts']

        # Assert the response data
        assert_post_list(self, data, expected_count=n - b - c)

    def test_read_posts_empty(self):
        # Get the posts
        response = self.GETRequest(self.route)

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=10,
            expected_total=0
        )

        # Get the response data
        posts = pagination['posts']

        # Assert the response data
        assert_post_list(self, posts, expected_count=0)

    def test_read_posts_empty_args(self):
        # Get the posts
        response = self.GETRequest(
            self.route,
            query_string={'page': 1, 'per_page': 5}
        )

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=5,
            expected_total=0
        )

        # Get the response data
        posts = pagination['posts']

        # Assert the response data
        assert_post_list(self, posts, expected_count=0)
