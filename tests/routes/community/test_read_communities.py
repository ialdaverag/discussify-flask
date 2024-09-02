# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.assert_pagination import assert_pagination_structure_communities
from tests.utils.assert_list import assert_community_list


class TestReadCommunities(BaseTestCase):
    route = '/community/'

    def test_read_communities(self):
        # Number of communities
        n = 5

        # Create multiple communities
        CommunityFactory.create_batch(n)

        # Get the communities
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_communities(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=1, 
            expected_per_page=10, 
            expected_total=n
        )

        # Get the communities
        communities = pagination['communities']

        # Assert the communities
        assert_community_list(self, communities, n)

    def test_read_communities_args(self):
        # Number of communities
        n = 5

        # Create multiple communities
        CommunityFactory.create_batch(n)

        # Get the communities
        response = self.client.get(
            self.route,
            query_string={
                'page': 1,
                'per_page': 2
            }
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_communities(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=3, 
            expected_per_page=2, 
            expected_total=n
        )

        # Get the communities
        communities = pagination['communities']

        # Assert the communities
        assert_community_list(self, communities, 2)

    def test_read_communities_empty(self):
        # Get the communities
        response = self.client.get(self.route)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_communities(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=0, 
            expected_per_page=10, 
            expected_total=0
        )

        # Get the communities
        communities = pagination['communities']

        # Assert the communities
        assert_community_list(self, communities)

    def test_read_communities_empty_args(self):
        # Get the communities
        response = self.client.get(
            self.route,
            query_string={
                'page': 1,
                'per_page': 2
            }
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the pagination
        pagination = response.json

        # Assert the pagination
        assert_pagination_structure_communities(
            self, 
            pagination, 
            expected_page=1, 
            expected_pages=0, 
            expected_per_page=2, 
            expected_total=0
        )

        # Get the communities
        communities = pagination['communities']

        # Assert the communities
        assert_community_list(self, communities)
