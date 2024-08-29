# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.post_factory import PostFactory
from tests.factories.comment_factory import CommentFactory
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Block
from app.models.community import CommunityModerator

# Utils
from tests.utils.tokens import get_access_token


class TestReadComments(BaseTestCase):
    route = '/post/{}/comments'

    def test_read_comments(self):
        # Number of comments
        n = 5

        # Create a post
        post = PostFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n, post=post)

        # Get the comments
        response = self.client.get(
            self.route.format(post.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of comments
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for comment in data:
            self.assertIn('id', comment)
            self.assertIn('content', comment)
            self.assertIn('owner', comment)
            self.assertIn('post', comment)
            self.assertIn('bookmarked', comment)
            self.assertIn('upvoted', comment)
            self.assertIn('downvoted', comment)
            self.assertIn('stats', comment)
            self.assertIn('created_at', comment)
            self.assertIn('updated_at', comment)

    def test_read_comments_as_user(self):
        # Number of comments
        n = 5

        # Create a post
        post = PostFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n, post=post)

        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Get the comments
        response = self.client.get(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of comments
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for comment in data:
            self.assertIn('id', comment)
            self.assertIn('content', comment)
            self.assertIn('owner', comment)
            self.assertIn('post', comment)
            self.assertIn('bookmarked', comment)
            self.assertIn('upvoted', comment)
            self.assertIn('downvoted', comment)
            self.assertIn('stats', comment)
            self.assertIn('created_at', comment)
            self.assertIn('updated_at', comment)

    def test_read_comments_as_user_with_blocked(self):
        # Number of comments
        n = 5

        # Create a post
        post = PostFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n, post=post)

        # Create a user
        user = UserFactory()

        # Number of blocked users
        b = 2

        # Make the blocked users block the user
        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the comments
        response = self.client.get(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of comments
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
        for comment in data:
            self.assertIn('id', comment)
            self.assertIn('content', comment)
            self.assertIn('owner', comment)
            self.assertIn('post', comment)
            self.assertIn('bookmarked', comment)
            self.assertIn('upvoted', comment)
            self.assertIn('downvoted', comment)
            self.assertIn('stats', comment)
            self.assertIn('created_at', comment)
            self.assertIn('updated_at', comment)

    def test_read_comments_as_user_with_blockers(self):
        # Number of comments
        n = 5

        # Create a post
        post = PostFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n, post=post)

        # Create a user
        user = UserFactory()

        # Number of blockers
        b = 2

        # Make the user block the blockers
        for comment in comments[:b]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the comments
        response = self.client.get(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of comments
        self.assertEqual(len(data), n - b)

        # Assert the response data structure
        for comment in data:
            self.assertIn('id', comment)
            self.assertIn('content', comment)
            self.assertIn('owner', comment)
            self.assertIn('post', comment)
            self.assertIn('bookmarked', comment)
            self.assertIn('upvoted', comment)
            self.assertIn('downvoted', comment)
            self.assertIn('stats', comment)
            self.assertIn('created_at', comment)
            self.assertIn('updated_at', comment)

    def test_read_comments_as_user_with_blocked_and_blockers(self):
        # Number of comments
        n = 5

        # Create a post
        post = PostFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n, post=post)

        # Create a user
        user = UserFactory()

        # Number of blocked users
        b = 2

        # Make the blocked users block the user
        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Number of blockers
        c = 2

        # Make the user block the blockers
        for comment in comments[-c:]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the comments
        response = self.client.get(
            self.route.format(post.id),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

        # Assert the number of comments
        self.assertEqual(len(data), n - b - c)

        # Assert the response data structure
        for comment in data:
            self.assertIn('id', comment)
            self.assertIn('content', comment)
            self.assertIn('owner', comment)
            self.assertIn('post', comment)
            self.assertIn('bookmarked', comment)
            self.assertIn('upvoted', comment)
            self.assertIn('downvoted', comment)
            self.assertIn('stats', comment)
            self.assertIn('created_at', comment)
            self.assertIn('updated_at', comment)
    
    def test_read_comments_as_moderator(self):
        # Number of posts
        n = 5

        # Create a post 
        post = PostFactory()

        # Create multiple posts
        comments = CommentFactory.create_batch(n, post=post)

        # Create a moderator
        user = UserFactory()

        # Get the post's community
        community = post.community

        # Add the user as a moderator
        CommunityModerator(user=user, community=community).save()

        # Number of blocked users
        b = 2

        # Make the blocked users block the moderator
        for comment in comments[:b]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Read the community posts
        response = self.client.get(
            self.route.format(post.id), 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for comment in data:
            self.assertIn('id', comment)
            self.assertIn('content', comment)
            self.assertIn('owner', comment)
            self.assertIn('post', comment)
            self.assertIn('bookmarked', comment)
            self.assertIn('upvoted', comment)
            self.assertIn('downvoted', comment)
            self.assertIn('stats', comment)
            self.assertIn('created_at', comment)
            self.assertIn('updated_at', comment)

    def test_read_comments_as_moderator_with_blockers(self):
        # Number of posts
        n = 5

        # Create a post 
        post = PostFactory()

        # Create multiple posts
        comments = CommentFactory.create_batch(n, post=post)

        # Create a moderator
        user = UserFactory()

        # Get the post's community
        community = post.community

        # Add the user as a moderator
        CommunityModerator(user=user, community=community).save()

        # Number of blocked users
        b = 2

        # Make the blocked users block the moderator
        for comment in comments[:b]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Read the community posts
        response = self.client.get(
            self.route.format(post.id), 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n)

        # Assert the response data structure
        for comment in data:
            self.assertIn('id', comment)
            self.assertIn('content', comment)
            self.assertIn('owner', comment)
            self.assertIn('post', comment)
            self.assertIn('bookmarked', comment)
            self.assertIn('upvoted', comment)
            self.assertIn('downvoted', comment)
            self.assertIn('stats', comment)
            self.assertIn('created_at', comment)
            self.assertIn('updated_at', comment)

    def test_read_comments_as_moderator_with_blocked_and_blockers(self):
        # Number of posts
        n = 5

        # Create a post 
        post = PostFactory()

        # Create multiple posts
        comments = CommentFactory.create_batch(n, post=post)

        # Create a moderator
        user = UserFactory()

        # Get the post's community
        community = post.community

        # Add the user as a moderator
        CommunityModerator(user=user, community=community).save()

        # Number of blocked users
        b = 2

        # Make the blocked users block the moderator
        for comment in comments[:b]:
            Block(blocker=comment.owner, blocked=user).save()

        # Number of blockers
        c = 2

        # Make the moderator block the blocked users
        for comment in comments[-c:]:
            Block(blocker=user, blocked=comment.owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Read the community posts
        response = self.client.get(
            self.route.format(post.id), 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
        self.assertEqual(len(data), n)

    def test_read_comments_empty(self):
        # Create a post
        post = PostFactory()

        # Get the comments
        response = self.client.get(
            self.route.format(post.id)
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Get the data
        data = response.json

        # Assert that the response data is an empty list
        self.assertEqual(data, [])