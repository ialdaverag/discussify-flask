# Tests
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.community_factory import CommunityFactory
from tests.factories.post_factory import PostFactory
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Block
from app.models.community import CommunityModerator

# Utils
from tests.utils.tokens import get_access_token
from tests.utils.assert_pagination import assert_pagination_structure_posts
from tests.utils.assert_list import assert_post_list


class TestReadPosts(TestRoute):
    route = '/community/{}/posts'

    def test_read_posts(self):
        # Number of posts
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        PostFactory.create_batch(n, community=community)

        # Read the community posts
        response = self.GETRequest(self.route.format(community.name))

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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n)

    def test_read_posts_args(self):
        # Number of posts
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        PostFactory.create_batch(n, community=community)

        # Read the community posts
        response = self.GETRequest(self.route.format(community.name),
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
            expected_pages=1,
            expected_per_page=5,
            expected_total=n
        )

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n)

    def test_read_posts_as_user(self):
        # Number of posts
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        PostFactory.create_batch(n, community=community)

        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Read the community posts
        response = self.GETRequest(self.route.format(community.name), token=access_token)

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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n)

    def test_read_posts_as_user_args(self):
        # Number of posts
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        PostFactory.create_batch(n, community=community)

        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)

        # Read the community posts
        response = self.GETRequest(self.route.format(community.name),
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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n)

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
        response = self.GETRequest(self.route.format(community.name), token=access_token)

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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n - b)

    def test_read_posts_as_user_with_blocked_args(self):
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
        response = self.GETRequest(self.route.format(community.name),
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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n - b)

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
        response = self.GETRequest(self.route.format(community.name), token=access_token)

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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n - b)

    def test_read_posts_as_user_with_blockers_args(self):
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
        response = self.GETRequest(self.route.format(community.name),
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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n - b)
    
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
        response = self.GETRequest(self.route.format(community.name), token=access_token)

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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n - b - c)

    def test_read_posts_as_user_with_blocked_and_blockers_args(self):
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
        response = self.GETRequest(self.route.format(community.name),
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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n - b - c)

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
        response = self.GETRequest(self.route.format(community.name), token=access_token)

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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n)

    def test_read_posts_as_moderator_args(self):
        # Number of posts
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create multiple posts
        PostFactory.create_batch(n, community=community)

        # Create a moderator
        user = UserFactory()

        # Add the user as a moderator
        CommunityModerator(user=user, community=community).save()

        # Get the access token
        access_token = get_access_token(user)

        # Read the community posts
        response = self.GETRequest(self.route.format(community.name),
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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n)

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
        response = self.GETRequest(self.route.format(community.name), token=access_token)

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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n)

    def test_read_posts_as_moderator_with_blocked_args(self):
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
        response = self.GETRequest(self.route.format(community.name),
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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n)

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
        response = self.GETRequest(self.route.format(community.name), token=access_token)

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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n)

    def test_read_posts_as_moderator_with_blockers_args(self):
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
        response = self.GETRequest(self.route.format(community.name),
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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n)

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
        response = self.GETRequest(self.route.format(community.name), token=access_token)

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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n)

    def test_read_posts_as_moderator_with_blocked_and_blockers_args(self):
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
        response = self.GETRequest(self.route.format(community.name),
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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, n)

    def test_read_posts_empty(self):
        # Create a community
        community = CommunityFactory()

        # Read the community posts
        response = self.GETRequest(self.route.format(community.name))

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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, 0)

    def test_read_posts_empty_args(self):
        # Create a community
        community = CommunityFactory()

        # Read the community posts
        response = self.GETRequest(self.route.format(community.name),
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

        # Get the posts
        posts = pagination['posts']

        # Assert the posts list
        assert_post_list(self, posts, 0)

    def test_read_posts_nonexistent_community(self):
        # Try to get posts of a nonexistent community
        response = self.GETRequest(self.route.format('nonexistent'))

        # Assert the response status code
        self.assertStatusCode(response, 404)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Community not found.')
