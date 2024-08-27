# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Models
from app.models.post import PostVote
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadDownvotedPosts(BaseTestCase):
    route = '/user/posts/downvoted'

    def test_read_downvoted_posts(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user downvote the posts
        for post in posts:
            PostVote(user=user, post=post, direction=-1).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user downvoted posts
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of downvotes
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for post in data:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('owner', post)
            self.assertIn('community', post)
            self.assertIn('bookmarked', post)
            self.assertIn('upvoted', post)
            self.assertIn('downvoted', post)
            self.assertIn('stats', post)
            self.assertIn('created_at', post)
            self.assertIn('updated_at', post)

    def test_read_downvoted_posts_with_blocked(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user downvote the posts
        for post in posts:
            PostVote(user=user, post=post, direction=-1).save()

        # Number of blocked users
        b = 2

        for post in posts[:b]:
            Block(blocker=user, blocked=post.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user downvoted posts
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of downvotes
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
        for post in data:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('owner', post)
            self.assertIn('community', post)
            self.assertIn('bookmarked', post)
            self.assertIn('upvoted', post)
            self.assertIn('downvoted', post)
            self.assertIn('stats', post)
            self.assertIn('created_at', post)
            self.assertIn('updated_at', post)

    def test_read_downvoted_posts_with_blockers(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user downvote the posts
        for post in posts:
            PostVote(user=user, post=post, direction=-1).save()

        # Number of blocking users
        b = 2

        for post in posts[:b]:
            Block(blocker=post.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user downvoted posts
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of downvotes
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
        for post in data:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('owner', post)
            self.assertIn('community', post)
            self.assertIn('bookmarked', post)
            self.assertIn('upvoted', post)
            self.assertIn('downvoted', post)
            self.assertIn('stats', post)
            self.assertIn('created_at', post)
            self.assertIn('updated_at', post)

    def test_read_downvoted_posts_with_blocked_and_blockers(self):
        # Number of posts
        n = 5

        # Create a user
        user = UserFactory()

        # Create some posts
        posts = PostFactory.create_batch(n)

        # Make the user downvote the posts
        for post in posts:
            PostVote(user=user, post=post, direction=-1).save()

        # Number of blocked users
        b = 2

        for post in posts[:b]:
            Block(blocker=user, blocked=post.owner).save()

        # Number of blockers
        c = 2

        for post in posts[-c:]:
            Block(blocker=post.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user downvoted posts
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of downvotes
        self.assertEqual(len(data), n - b - c)

        # Assert the response data structure
        for post in data:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('owner', post)
            self.assertIn('community', post)
            self.assertIn('bookmarked', post)
            self.assertIn('upvoted', post)
            self.assertIn('downvoted', post)
            self.assertIn('stats', post)
            self.assertIn('created_at', post)
            self.assertIn('updated_at', post)

    def test_read_downvoted_posts_empty(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user downvoted posts
        response = self.client.get(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is an empty list
        self.assertEqual(data, [])