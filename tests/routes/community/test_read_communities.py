# Tests
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.community_factory import CommunityFactory


class TestReadCommunities(BasePaginationTest):
    route = '/community/'

    def test_read_communities(self):
        # Number of communities
        n = 5

        # Create multiple communities
        CommunityFactory.create_batch(n)

        # Get the communities
        response = self.GETRequest(self.route)

        # Assert standard pagination response
        self.assert_standard_pagination_response(response, expected_total=n, data_key='communities')

    def test_read_communities_args(self):
        # Number of communities
        n = 5

        # Create multiple communities
        CommunityFactory.create_batch(n)

        # Get the communities with pagination arguments
        response = self.GETRequest(
            self.route,
            query_string={
                'page': 1,
                'per_page': 2
            }
        )

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=1, 
            per_page=2, 
            expected_total=n, 
            data_key='communities'
        )

    def test_read_communities_empty(self):
        # Get the communities (no communities created)
        response = self.GETRequest(self.route)

        # Assert standard pagination response with 0 total
        self.assert_standard_pagination_response(response, expected_total=0, data_key='communities')

    def test_read_communities_empty_args(self):
        # Get the communities with pagination arguments (no communities created)
        response = self.GETRequest(
            self.route,
            query_string={
                'page': 1,
                'per_page': 2
            }
        )

        # Assert paginated response with 0 total
        self.assert_paginated_response(
            response=response,
            page=1, 
            per_page=2, 
            expected_total=0, 
            data_key='communities'
        )
