# Tests
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityModerator
from tests.utils.assert_pagination import assert_pagination_structure
from tests.utils.assert_list import assert_user_list


class TestReadModerators(TestRoute):
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

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
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

        # Get the users
        data = pagination['users']

        # Assert the users
        assert_user_list(self, data, expected_count=n)

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

        # Set args
        args = {'page': 1, 'per_page': 2}

        # Read the community moderators
        response = self.GETRequest(self.route.format(community.name), 
            query_string=args
        )

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=3,
            expected_per_page=2,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, expected_count=2)

    def test_read_moderators_empty(self):
        # Create a community
        community = CommunityFactory()

        # Read the community moderators
        response = self.GETRequest(self.route.format(community.name))

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
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

        # Get response data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, expected_count=0)

    def test_read_moderators_empty_args(self):
        # Create a community
        community = CommunityFactory()

        # Set args
        args = {'page': 1, 'per_page': 2}

        # Read the community moderators
        response = self.GETRequest(self.route.format(community.name), 
            query_string=args
        )

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=2,
            expected_total=0
        )

        # Get response data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, expected_count=0)

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
