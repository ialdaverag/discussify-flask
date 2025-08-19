# tests
from tests.routes.test_route import TestRoute

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.post import PostVote

# utils
from tests.utils.tokens import get_access_token
from tests.utils.assert_pagination import assert_pagination_structure_posts
from tests.utils.assert_list import assert_post_list

# Models
from app.models.user import Block


class TestReadUpvotedPosts(TestRoute):
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

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get pagination
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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n)

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

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=2,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n
        )

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, 5)

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

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get pagination
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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n - b)

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

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=2,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, 5)

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

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get pagination
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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n - b)

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

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=2,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, 5)

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

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get pagination
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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n - b - c)

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

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=2,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b - c
        )

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, 5)

    def test_read_upvoted_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user upvoted posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get pagination
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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts)

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

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=2,
            expected_pages=0,
            expected_per_page=5,
            expected_total=0
        )

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts)