# tests
from tests.base.base_pagination_test import BasePaginationTest

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.post import PostVote
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadUpvotedPosts(BasePaginationTest):
    route = '/user/posts/upvoted'

    def test_read_upvoted_posts(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user upvote the posts
        for post in posts:
            PostVote(user=user, post=post, direction=1).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response for posts
        self.assert_standard_pagination_response(response, expected_total=n, data_key='posts')

    def test_read_upvoted_posts_args(self):
        # Number of posts
        n = 15

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user upvote the posts
        for post in posts:
            PostVote(user=user, post=post, direction=1).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted posts
        response = self.GETRequest(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=2,
            per_page=5,
            expected_total=n,
            data_key='posts'
        )

    def test_read_upvoted_posts_with_blocked(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user upvote the posts
        for post in posts:
            PostVote(user=user, post=post, direction=1).save()

        # Number of blocked users
        b = 2

        for post in posts[:b]:
            Block(blocker=user, blocked=post.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n - b, data_key='posts')

    def test_read_upvoted_posts_with_blocked_args(self):
        # Number of posts
        n = 15

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user upvote the posts
        for post in posts:
            PostVote(user=user, post=post, direction=1).save()

        # Number of blocked users
        b = 2

        for post in posts[:b]:
            Block(blocker=user, blocked=post.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted posts
        response = self.GETRequest(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=2,
            per_page=5,
            expected_total=n - b,
            data_key='posts'
        )

    def test_read_upvoted_posts_with_blockers(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user upvote the posts
        for post in posts:
            PostVote(user=user, post=post, direction=1).save()

        # Number of blocking users
        b = 2

        for post in posts[:b]:
            Block(blocker=post.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n - b, data_key='posts')

    def test_read_upvoted_posts_with_blockers_args(self):
        # Number of posts
        n = 15

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user upvote the posts
        for post in posts:
            PostVote(user=user, post=post, direction=1).save()

        # Number of blocking users
        b = 2

        for post in posts[:b]:
            Block(blocker=post.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted posts
        response = self.GETRequest(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=2,
            per_page=5,
            expected_total=n - b,
            data_key='posts'
        )

    def test_read_upvoted_posts_with_blocked_and_blockers(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user upvote the posts
        for post in posts:
            PostVote(user=user, post=post, direction=1).save()

        # Number of blocked users
        b = 2

        for post in posts[:b]:
            Block(blocker=user, blocked=post.owner).save()

        # Number of blockers users
        c = 2

        for post in posts[-c:]:
            Block(blocker=post.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n - b - c, data_key='posts')

    def test_read_upvoted_posts_with_blocked_and_blockers_args(self):
        # Number of posts
        n = 15

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user upvote the posts
        for post in posts:
            PostVote(user=user, post=post, direction=1).save()

        # Number of blocked users
        b = 2

        for post in posts[:b]:
            Block(blocker=user, blocked=post.owner).save()

        # Number of blockers users
        c = 2

        for post in posts[-c:]:
            Block(blocker=post.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted posts
        response = self.GETRequest(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=2,
            per_page=5,
            expected_total=n - b - c,
            data_key='posts'
        )

    def test_read_upvoted_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user upvoted posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response with 0 total
        self.assert_standard_pagination_response(response, expected_total=0, data_key='posts')

    def test_read_upvoted_posts_empty_args(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user upvoted posts
        response = self.GETRequest(
            self.route,
            query_string={'page': 2, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert paginated response with 0 total
        self.assert_paginated_response(
            response=response,
            page=2,
            per_page=5,
            expected_total=0,
            data_key='posts'
        )