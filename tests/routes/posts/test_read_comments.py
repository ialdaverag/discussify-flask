# Base
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.post_factory import PostFactory
from tests.factories.comment_factory import CommentFactory
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Block
from app.models.community import CommunityModerator

# Utils
from tests.utils.tokens import get_access_token


class TestReadComments(BasePaginationTest):
    route = '/post/{}/comments'

    def test_read_comments(self):
        # Number of comments
        n = 5

        # Create a post
        post = PostFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n, post=post)

        # Get the comments
        response = self.GETRequest(self.route.format(post.id)
        )

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments list
        assert_comment_list(self, comments, n)

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
        response = self.GETRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments list
        assert_comment_list(self, comments, n)

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
        response = self.GETRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments list
        assert_comment_list(self, comments, n - b)

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
        response = self.GETRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments list
        assert_comment_list(self, comments, n - b)

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
        response = self.GETRequest(self.route.format(post.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b - c
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments list
        assert_comment_list(self, comments, n - b - c)
    
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
        response = self.GETRequest(self.route.format(post.id), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments list
        assert_comment_list(self, comments, n)

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
        response = self.GETRequest(self.route.format(post.id), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments list
        assert_comment_list(self, comments, n)

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
        response = self.GETRequest(self.route.format(post.id), token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments list
        assert_comment_list(self, comments, n)

    def test_read_comments_empty(self):
        # Create a post
        post = PostFactory()

        # Get the comments
        response = self.GETRequest(self.route.format(post.id)
        )

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination structure
        assert_pagination_structure_comments(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=10,
            expected_total=0
        )

        # Get the comments
        comments = pagination['comments']

        # Assert the comments list
        assert_comment_list(self, comments)