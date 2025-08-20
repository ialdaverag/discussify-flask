# Tests
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityModerator


class TestReadModerators(BasePaginationTest):
    route = '/community/{}/moderators'

    def test_read_moderators(self):
        # Number of moderators
        n = 5

        # Create multiple moderators
        moderators = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the moderators to the community
        for moderator in moderators:
            CommunityModerator(community=community, user=moderator).save()

        # Read the community moderators
        response = self.GETRequest(self.route.format(community.name))

        # Assert standard pagination response for users
        self.assert_standard_pagination_response(response, expected_total=n, data_key='users')

    def test_read_moderators_args(self):
        # Number of moderators
        n = 5

        # Create multiple moderators
        moderators = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the moderators to the community
        for moderator in moderators:
            CommunityModerator(community=community, user=moderator).save()

        # Read the community moderators with pagination
        response = self.GETRequest(self.route.format(community.name), 
            query_string={'page': 1, 'per_page': 2}
        )

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=2,
            expected_total=n,
            data_key='users'
        )

    def test_read_moderators_empty(self):
        # Create a community
        community = CommunityFactory()

        # Read the community moderators
        response = self.GETRequest(self.route.format(community.name))

        # Assert standard pagination response with 0 total
        self.assert_standard_pagination_response(response, expected_total=0, data_key='users')

    def test_read_moderators_empty_args(self):
        # Create a community
        community = CommunityFactory()

        # Read the community moderators with pagination
        response = self.GETRequest(self.route.format(community.name), 
            query_string={'page': 1, 'per_page': 2}
        )

        # Assert paginated response with 0 total
        self.assert_paginated_response(
            response=response,
            page=1,
            per_page=2,
            expected_total=0,
            data_key='users'
        )

    def test_read_moderators_nonexistent_community(self):
        # Try to get moderators of a nonexistent community
        response = self.GETRequest(self.route.format('nonexistent'))

        # Assert the response status code
        self.assertStatusCode(response, 404)

        # Get response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Community not found.')
