# tests
from tests.routes.test_route import TestRoute

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_bookmark_factory import PostBookmarkFactory
from tests.factories.user_factory import UserFactory
from tests.factories.block_factory import BlockFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token
from tests.utils.assert_pagination import assert_pagination_structure_posts
from tests.utils.assert_list import assert_post_list


class TestReadBookmarkedPosts(TestRoute):
    route = '/user/posts/bookmarked'

    def test_read_bookmarked_posts(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        PostBookmarkFactory.create_batch(n, user=user)

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get pagination data
        pagination = response.json

         # Assert pagination data structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get posts
        posts = pagination['posts']

        # Assert posts list
        assert_post_list(self, posts, n)

    def test_read_bookmarked_posts_args(self):
        # Number of posts
        n = 15

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        PostBookmarkFactory.create_batch(n, user=user)

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.GETRequest(f'{self.route}?page=1&per_page=5', token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get pagination data
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n
        )

        # Get posts
        posts = pagination['posts']

        # Assert posts list
        assert_post_list(self, posts, 5)

    def test_read_bookmarked_posts_with_blocked(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = PostBookmarkFactory.create_batch(n, user=user)

        # Number of blocked users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=user, blocked=bookmark.post.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get posts
        posts = pagination['posts']

        # Assert posts list
        assert_post_list(self, posts, n - b)

    def test_read_bookmarked_posts_with_blocked_args(self):
        # Number of posts
        n = 15

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = PostBookmarkFactory.create_batch(n, user=user)

        # Number of blocked users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=user, blocked=bookmark.post.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.GETRequest(f'{self.route}?page=1&per_page=5', token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get posts
        posts = pagination['posts']

        # Assert posts list
        assert_post_list(self, posts, 5)

    def test_read_bookmarked_posts_with_blockers(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = PostBookmarkFactory.create_batch(n, user=user)

        # Number of blocking users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=bookmark.post.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get posts
        posts = pagination['posts']

        # Assert posts list
        assert_post_list(self, posts, n - b)

    def test_read_bookmarked_posts_with_blockers_args(self):
        # Number of posts
        n = 15

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = PostBookmarkFactory.create_batch(n, user=user)

        # Number of blocking users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=bookmark.post.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.GETRequest(f'{self.route}?page=1&per_page=5', token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get posts
        posts = pagination['posts']

        # Assert posts list
        assert_post_list(self, posts, 5)

    def test_read_bookmarked_posts_with_blocked_and_blockers(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = PostBookmarkFactory.create_batch(n, user=user)

        # Number of blocking users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=bookmark.post.owner, blocked=user).save()

        # Number of blocked users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=user, blocked=bookmark.post.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get posts
        posts = pagination['posts']

        # Assert posts list
        assert_post_list(self, posts, n - b)

    def test_read_bookmarked_posts_with_blocked_and_blockers_args(self):
        # Number of posts
        n = 15

        # Create a user
        user = UserFactory()

        # Create some bookmarks
        bookmarks = PostBookmarkFactory.create_batch(n, user=user)

        # Number of blocking users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=bookmark.post.owner, blocked=user).save()

        # Number of blocked users
        b = 2

        for bookmark in bookmarks[:b]:
            Block(blocker=user, blocked=bookmark.post.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.GETRequest(f'{self.route}?page=1&per_page=5', token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get posts
        posts = pagination['posts']

        # Assert posts list
        assert_post_list(self, posts, 5)

    def test_read_bookmarked_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.GETRequest(self.route, token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=10,
            expected_total=0
        )

        # Get posts
        posts = pagination['posts']

        # Assert posts list
        assert_post_list(self, posts)

    def test_read_bookmarked_posts_empty_args(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user bookmarked posts
        response = self.GETRequest(f'{self.route}?page=1&per_page=5', token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get pagination
        pagination = response.json

        # Assert pagination data structure
        assert_pagination_structure_posts(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=5,
            expected_total=0
        )

        # Get posts
        posts = pagination['posts']

        # Assert posts list
        assert_post_list(self, posts)