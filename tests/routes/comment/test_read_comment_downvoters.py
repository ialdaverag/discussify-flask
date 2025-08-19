# Base
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_vote_factory import CommentVoteFactory
from tests.factories.comment_factory import CommentFactory

# Models
from app.models.user import Block

# Utils
from tests.utils.tokens import get_access_token
from tests.utils.assert_pagination import assert_pagination_structure
from tests.utils.assert_list import assert_user_list


class TestReadCommentDownvoters(TestRoute):
    route = '/comment/{}/downvoters'

    def test_read_comment_downvoters(self):
        # Number of downvoters
        n = 5

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Get the downvoters
        response = self.GETRequest(self.route.format(comment.id))

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=1, 
            expected_per_page=10, 
            expected_total=n
        )

        # Get the downvoters
        downvoters = pagination['users']

        # Assert the downvoters list
        assert_user_list(self, downvoters, n)

    def test_read_comment_downvoters_args(self):
        # Number of downvoters
        n = 5

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Get the downvoters
        response = self.GETRequest(self.route.format(comment.id),
            query_string={'page': 1, 'per_page': 5}
        )

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=1, 
            expected_per_page=5, 
            expected_total=n
        )

        # Get the downvoters
        downvoters = pagination['users']

        # Assert the downvoters list
        assert_user_list(self, downvoters, n)

    def test_read_commentt_downvoters_authenticated(self):
        # Number of downvoters
        n = 5

        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
        response = self.GETRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=1, 
            expected_per_page=10, 
            expected_total=n
        )

        # Get the downvoters
        downvoters = pagination['users']

        # Assert the downvoters list
        assert_user_list(self, downvoters, n)

    def test_read_comment_downvoters_authenticated_args(self):
        # Number of downvoters
        n = 5

        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
        response = self.GETRequest(self.route.format(comment.id),
            query_string={'page': 1, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=1, 
            expected_per_page=5, 
            expected_total=n
        )

        # Get the downvoters
        downvoters = pagination['users']

        # Assert the downvoters list
        assert_user_list(self, downvoters, n)

    def test_read_comment_downvoters_with_blocked(self):
        # Number of downvoters
        n = 5

        # Number of blocked downvoters
        b = 2

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        downvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Create a user
        user = UserFactory()

        # Block the downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=user, blocked=downvoter.user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
        response = self.GETRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=1, 
            expected_per_page=10, 
            expected_total=n - b
        )

        # Get the downvoters
        downvoters = pagination['users']

        # Assert the downvoters list
        assert_user_list(self, downvoters, n - b)

    def test_read_comment_downvoters_with_blocked_args(self):
        # Number of downvoters
        n = 5

        # Number of blocked downvoters
        b = 2

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        downvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Create a user
        user = UserFactory()

        # Block the downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=user, blocked=downvoter.user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
        response = self.GETRequest(self.route.format(comment.id),
            query_string={'page': 1, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=1, 
            expected_per_page=5, 
            expected_total=n - b
        )

        # Get the downvoters
        downvoters = pagination['users']

        # Assert the downvoters list
        assert_user_list(self, downvoters, n - b)

    def test_read_comment_downvoters_with_blockers(self):
        # Number of downvoters
        n = 5

        # Number of blockers
        b = 3

        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        downvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Block the user from the first 3 downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=downvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
        response = self.GETRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get the downvoters
        downvoters = pagination['users']

        # Assert the downvoters list
        assert_user_list(self, downvoters, n - b)

    def test_read_comment_downvoters_with_blockers_args(self):
        # Number of downvoters
        n = 5

        # Number of blockers
        b = 3

        # Create a user
        user = UserFactory()

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        downvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Block the user from the first 3 downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=downvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
        response = self.GETRequest(self.route.format(comment.id),
            query_string={'page': 1, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get the downvoters
        downvoters = pagination['users']

        # Assert the downvoters list
        assert_user_list(self, downvoters, n - b)

    def test_read_comment_downvoters_with_blocked_and_blockers(self):
        # Number of downvoters
        n = 5

        # Number of blocked downvoters
        b = 2

        # Number of blockers
        c = 2

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        downvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Create a user
        user = UserFactory()

        # Block the downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=user, blocked=downvoter.user).save()

        # Block the user
        for downvoter in downvoters[-c:]:
            Block(blocker=downvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
        response = self.GETRequest(self.route.format(comment.id), token=access_token)

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b - c
        )

        # Get the downvoters
        downvoters = pagination['users']

        # Assert the downvoters list
        assert_user_list(self, downvoters, n - b - c)

    def test_read_comment_downvoters_with_blocked_and_blockers_args(self):
        # Number of downvoters
        n = 5

        # Number of blocked downvoters
        b = 2

        # Number of blockers
        c = 2

        # Create a comment
        comment = CommentFactory()

        # Create some downvoters
        downvoters = CommentVoteFactory.create_batch(n, comment=comment, direction=-1)

        # Create a user
        user = UserFactory()

        # Block the downvoters
        for downvoter in downvoters[:b]:
            Block(blocker=user, blocked=downvoter.user).save()

        # Block the user
        for downvoter in downvoters[-c:]:
            Block(blocker=downvoter.user, blocked=user).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the downvoters
        response = self.GETRequest(self.route.format(comment.id),
            query_string={'page': 1, 'per_page': 5},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n - b - c
        )

        # Get the downvoters
        downvoters = pagination['users']

        # Assert the downvoters list
        assert_user_list(self, downvoters, n - b - c)

    def test_read_comment_downvoters_empty(self):
        # Create a comment
        comment = CommentFactory()

        # Get the downvoters
        response = self.GETRequest(self.route.format(comment.id))

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=10,
            expected_total=0
        )

        # Get the downvoters
        downvoters = pagination['users']

        # Assert the downvoters list
        assert_user_list(self, downvoters, 0)

    def test_read_comment_downvoters_empty_args(self):
        # Create a comment
        comment = CommentFactory()

        # Get the downvoters
        response = self.GETRequest(self.route.format(comment.id),
            query_string={'page': 1, 'per_page': 5}
        )

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=5,
            expected_total=0
        )

        # Get the downvoters
        downvoters = pagination['users']

        # Assert the downvoters list
        assert_user_list(self, downvoters, 0)

    def test_read_comment_downvoters_nonexistent(self):
        # Get the downvoters
        response = self.GETRequest(self.route.format(404))

        # Check status code
        self.assertStatusCode(response, 404)
