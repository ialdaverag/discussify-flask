# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityModerator
from app.models.community import CommunityBan

# Utils
from tests.utils.tokens import get_access_token
from tests.utils.assert_pagination import assert_pagination_structure
from tests.utils.assert_list import assert_user_list


class TestReadBanned(BaseTestCase):
    route = '/community/{}/banned'

    def test_read_banned(self):
        # Number of banned users
        n = 5

        # Create a user
        users = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Get the owner of the community
        owner = community.owner

        # Append the owner to the community moderators
        CommunityModerator(community=community, user=owner).save()

        # Get the access token
        access_token = get_access_token(owner)

        # Append the users to the community banned users
        for user in users:
            CommunityBan(community=community, user=user).save()

        # Read the community banned users
        response = self.client.get(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

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

        # Assert list
        assert_user_list(self, data, expected_count=n)

    def test_read_banned_args(self):
        # Number of banned users
        n = 15

        # Create a user
        users = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Get the owner of the community
        owner = community.owner

        # Append the owner to the community moderators
        CommunityModerator(community=community, user=owner).save()

        # Get the access token
        access_token = get_access_token(owner)

        # Append the users to the community banned users
        for user in users:
            CommunityBan(community=community, user=user).save()

        # Set args
        args = {
            'page': 2,
            'per_page': 5
        }

        # Read the community banned users
        response = self.client.get(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'},
            query_string=args
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=2,
            expected_pages=3,
            expected_per_page=5,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, expected_count=5)

    def test_read_banned_empty(self):
        # Create a community
        community = CommunityFactory()

        # Get the owner of the community
        owner = community.owner

        # Get the access token
        access_token = get_access_token(owner)

        # Read the community banned users
        response = self.client.get(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

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

    def test_read_banned_empty_args(self):
        # Create a community
        community = CommunityFactory()

        # Get the owner of the community
        owner = community.owner

        # Get the access token
        access_token = get_access_token(owner)

        # Set args
        args = {'page': 1, 'per_page': 2}

        # Read the community banned users
        response = self.client.get(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'},
            query_string=args
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

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

    def test_read_banned_nonexistent_community(self):
        # Try to get banned users of a nonexistent community
        response = self.client.get(self.route.format('nonexistent'))

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert the keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Community not found.')
        