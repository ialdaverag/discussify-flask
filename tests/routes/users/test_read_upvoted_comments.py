# tests
from tests.base.base_pagination_test import BasePaginationTest

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory

# Models
from app.models.comment import CommentVote
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadUpvotedCommens(BasePaginationTest):
    route = '/user/comments/upvoted'

    def test_read_upvoted_comments(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user upvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=1).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted comments
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response for comments
        self.assert_standard_pagination_response(response, expected_total=n, data_key='comments')

    def test_read_upvoted_comments_args(self):
        # Number of comments
        n = 15

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user upvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=1).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted comments
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
            data_key='comments'
        )

    def test_read_upvoted_comments_with_blocked(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user upvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=1).save()

        # Number of blocked users
        b = 2

        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted comments
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n - b, data_key='comments')

    def test_read_upvoted_comments_with_blocked_args(self):
        # Number of comments
        n = 15

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user upvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=1).save()

        # Number of blocked users
        b = 2

        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted comments
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
            data_key='comments'
        )

    def test_read_upvoted_comments_with_blockers(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user upvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=1).save()

        # Number of blocking users
        b = 2

        for comment in comments[:b]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted comments
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n - b, data_key='comments')

    def test_read_upvoted_comments_with_blockers_args(self):
        # Number of comments
        n = 15

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user upvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=1).save()

        # Number of blocking users
        b = 2

        for comment in comments[:b]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted comments
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
            data_key='comments'
        )

    def test_read_upvoted_comments_with_blocked_and_blockers(self):
        # Number of comments
        n = 5

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user upvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=1).save()

        # Number of blocked users
        b = 2

        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Number of blockers users
        c = 2

        for comment in comments[-c:]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted comments
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n - b - c, data_key='comments')

    def test_read_upvoted_comments_with_blocked_and_blockers_args(self):
        # Number of comments
        n = 15

        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(n)

        # Make the user upvote the comments
        for comment in comments:
            CommentVote(user=user, comment=comment, direction=1).save()

        # Number of blocked users
        b = 2

        for comment in comments[:b]:
            Block(blocker=user, blocked=comment.owner).save()

        # Number of blockers users
        c = 2

        for comment in comments[-c:]:
            Block(blocker=comment.owner, blocked=user).save()

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted comments
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
            data_key='comments'
        )

    def test_read_upvoted_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user upvoted comments
        response = self.GETRequest(self.route, token=access_token)

        # Assert standard pagination response with 0 total
        self.assert_standard_pagination_response(response, expected_total=0, data_key='comments')

    def test_read_upvoted_comments_empty_args(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user upvoted comments
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
            data_key='comments'
        )