# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.post_factory import PostFactory
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadPosts(BasePaginationTest):
    route = '/post/'

    def test_read_posts(self):
        # Number of posts
        n = 5

        # Create multiple posts
        PostFactory.create_batch(n)

        # Get the posts
        response = self.GETRequest(self.route)

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n, data_key='posts')

    def test_read_posts_args(self):
        # Number of posts
        n = 5

        # Create multiple posts
        PostFactory.create_batch(n)

        # Get the posts with pagination
        response = self.GETRequest(
            self.route,
            query_string={'page': 1, 'per_page': 5}
        )

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=1, 
            per_page=5, 
            expected_total=n, 
            data_key='posts'
        )

    def test_read_posts_authenticated(self):
        # Number of posts
        n = 5

        # Create user and posts
        user, access_token = self.setup_authenticated_user()
        PostFactory.create_batch(n)

        # Get the posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n, data_key='posts')

    def test_read_posts_with_blocked(self):
        # Number of posts
        n = 5
        # Number of blocked users
        b = 2

        # Create user and posts
        user, access_token = self.setup_authenticated_user()
        posts = PostFactory.create_batch(n)

        # Block some post owners
        self.create_post_blocks(user, posts[:b])

        # Get the posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response (posts from non-blocked users)
        self.assert_standard_pagination_response(response, expected_total=n - b, data_key='posts')

    def test_read_posts_with_blockers(self):
        # Number of posts
        n = 5
        # Number of blockers
        b = 2

        # Create user and posts
        user, access_token = self.setup_authenticated_user()
        posts = PostFactory.create_batch(n)

        # Have some post owners block the user
        self.create_post_blockers(user, posts[:b])

        # Get the posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response (posts from non-blocking users)
        self.assert_standard_pagination_response(response, expected_total=n - b, data_key='posts')

    def test_read_posts_with_blocked_and_blockers(self):
        # Number of posts
        n = 5
        # Number of blocked users
        b = 2
        # Number of blockers
        c = 2

        # Create user and posts
        user, access_token = self.setup_authenticated_user()
        posts = PostFactory.create_batch(n)

        # Block some post owners and have others block the user
        self.create_post_blocks(user, posts[:b])
        self.create_post_blockers(user, posts[-c:])

        # Get the posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response (posts from available users)
        self.assert_standard_pagination_response(response, expected_total=n - b - c, data_key='posts')

    def test_read_posts_empty(self):
        # Get the posts (no posts created)
        response = self.GETRequest(self.route)

        # Assert standard pagination response with 0 total
        self.assert_standard_pagination_response(response, expected_total=0, data_key='posts')
