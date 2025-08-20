# tests
from tests.base.base_pagination_test import BasePaginationTest

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunitySubscriber


class TestReadSubscriptions(BasePaginationTest):
    route = '/user/{}/subscriptions'

    def test_read_subscriptions(self):
        # Number of communities
        n = 5

        # Create a user and communities
        user = UserFactory()
        communities = CommunityFactory.create_batch(n)

        # Make the user subscribe to the communities using helper
        self.create_subscriptions(user, communities)

        # Get user subscriptions
        response = self.GETRequest(self.route.format(user.username))

        # Assert standard pagination response for communities
        self.assert_standard_pagination_response(response, expected_total=n, data_key='communities')

    def test_read_subscriptions_args(self):
        # Number of communities
        n = 5

        # Create a user
        user = UserFactory()

        # Create some communities
        communities = CommunityFactory.create_batch(n)

        # Make the user subscribe to the communities
        for community in communities:
            CommunitySubscriber(community=community, user=user).save()

        # Get user subscriptions
        response = self.GETRequest(self.route.format(user.username),
            query_string={
                'page': 1,
                'per_page': 2
            }
        )

        # Assert paginated response for communities
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=2,
            expected_total=n,
            data_key='communities'
        )

    def test_read_subscriptions_empty(self):
        # Create a user
        user = UserFactory()

        # Get the user subscriptions
        response = self.GETRequest(self.route.format(user.username))

        # Assert standard pagination response with 0 total
        self.assert_standard_pagination_response(response, expected_total=0, data_key='communities')

    def test_read_subscriptions_empty_args(self):
        # Create a user
        user = UserFactory()

        # Get the user subscriptions
        response = self.GETRequest(self.route.format(user.username),
            query_string={
                'page': 1,
                'per_page': 10
            }
        )

        # Assert paginated response with 0 total
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=10,
            expected_total=0,
            data_key='communities'
        )

    def test_read_subscriptions_nonexistent_user(self):
        # Try to get subscriptions of a nonexistent user
        response = self.GETRequest(self.route.format('nonexistent'))

        # Assert the response status code
        self.assertStatusCode(response, 404)

        # Get response data
        data = response.json

        # Assert that message
        self.assertEqual(data['message'], 'User not found.')
