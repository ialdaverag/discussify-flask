# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.community_factory import CommunityFactory
from tests.factories.post_factory import PostFactory
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Block
from app.models.community import CommunityModerator

# Utils
from tests.utils.tokens import get_access_token

class TestReadPosts(BaseTestCase):
    route = '/community/{}/posts'

    def test_read_posts(self):
        # Number of posts
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        posts = PostFactory.create_batch(n, community=community)

        # Read the community posts
        response = self.client.get(self.route.format(community.name))

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
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

    def test_read_posts_as_user(self):
        # Number of posts
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        posts = PostFactory.create_batch(n, community=community)

        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Read the community posts
        response = self.client.get(
            self.route.format(community.name), 
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

    def test_read_posts_as_user_with_blocked(self):
        # Number of posts
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        posts = PostFactory.create_batch(n, community=community)

        # Create a user
        user = UserFactory()

        # Number of blocked users
        b = 2

        # Make the blocked users block the user
        for post in posts[:b]:
            Block(blocker=post.owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Read the community posts
        response = self.client.get(
            self.route.format(community.name), 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
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

    def test_read_posts_as_user_with_blockers(self):
        # Number of posts
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        posts = PostFactory.create_batch(n, community=community)

        # Create a user
        user = UserFactory()

        # Number of blockers
        b = 2

        # Make the blockers block the user
        for post in posts[-b:]:
            Block(blocker=post.owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Read the community posts
        response = self.client.get(
            self.route.format(community.name), 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
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
    
    def test_read_posts_as_user_with_blocked_and_blockers(self):
        # Number of posts
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        posts = PostFactory.create_batch(n, community=community)

        # Create a user
        user = UserFactory()

        # Number of blocked users
        b = 2

        # Make the blocked users block the user
        for post in posts[:b]:
            Block(blocker=post.owner, blocked=user).save()

        # Number of blockers
        c = 2

        # Make the blockers block the user
        for post in posts[-c:]:
            Block(blocker=user, blocked=post.owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Read the community posts
        response = self.client.get(
            self.route.format(community.name), 
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data is a list
        self.assertIsInstance(data, list)

        # Assert the response data length
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

    def test_read_posts_as_moderator(self):
        # Number of posts
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        posts = PostFactory.create_batch(n, community=community)

        # Create a moderator
        user = UserFactory()

        # Add the user as a moderator
        CommunityModerator(user=user, community=community).save()

        # Get the access token
        access_token = get_access_token(user)

        # Read the community posts
        response = self.client.get(
            self.route.format(community.name), 
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

    def test_read_posts_as_moderator_with_blocked(self):
        # Number of posts
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        posts = PostFactory.create_batch(n, community=community)

        # Create a moderator
        user = UserFactory()

        # Add the user as a moderator
        CommunityModerator(user=user, community=community).save()

        # Number of blocked users
        b = 2

        # Make the blocked users block the moderator
        for post in posts[:b]:
            Block(blocker=post.owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Read the community posts
        response = self.client.get(
            self.route.format(community.name), 
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

    def test_read_posts_as_moderator_with_blockers(self):
        # Number of posts
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        posts = PostFactory.create_batch(n, community=community)

        # Create a moderator
        user = UserFactory()

        # Add the user as a moderator
        CommunityModerator(user=user, community=community).save()

        # Number of blocked users
        b = 2

        # Make the blocked users block the moderator
        for post in posts[:b]:
            Block(blocker=user, blocked=post.owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Read the community posts
        response = self.client.get(
            self.route.format(community.name), 
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

    def test_read_posts_as_moderator_with_blocked_and_blockers(self):
        # Number of posts
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        posts = PostFactory.create_batch(n, community=community)

        # Create a moderator
        user = UserFactory()

        # Add the user as a moderator
        CommunityModerator(user=user, community=community).save()

        # Number of blocked users
        b = 2

        # Make the blocked users block the moderator
        for post in posts[:b]:
            Block(blocker=post.owner, blocked=user).save()

        # Number of blockers
        c = 2

        # Make the blocked users block the moderator
        for post in posts[-c:]:
            Block(blocker=user, blocked=post.owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Read the community posts
        response = self.client.get(
            self.route.format(community.name), 
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

    def test_read_posts_empty(self):
        # Create a community
        community = CommunityFactory()

        # Read the community posts
        response = self.client.get(self.route.format(community.name))

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data is an empty list
        self.assertEqual(data, [])

    def test_read_posts_nonexistent_community(self):
        # Try to get posts of a nonexistent community
        response = self.client.get(self.route.format('nonexistent'))

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Community not found.')
