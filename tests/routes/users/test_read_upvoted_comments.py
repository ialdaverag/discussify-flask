# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory

# utils
from tests.utils.tokens import get_access_token


class TestReadUpvotedComments(BaseTestCase):
    route = '/user/comments/upvoted'

    def test_read_upvoted_comments(self):
        # Create a user
        user = UserFactory()

        # Create some comments
        comments = CommentFactory.create_batch(5)

        # Make the user subscribe to the comments' communities
        for comment in comments:
            user.subscribe_to(comment.post.community)

        # Make the user upvote the comments
        for comment in comments:
            user.upvote_comment(comment)

        # Get user access token
        access_token = get_access_token(user)

        # Get user upvoted comments
        response = self.client.get(
            f'/user/comments/upvoted',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is a list
        self.assertIsInstance(data, list)

    def test_read_upvoted_comments_empty(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Get the user upvoted comments
        response = self.client.get(
            f'/user/comments/upvoted',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert that the response data is an empty list
        self.assertEqual(data, [])