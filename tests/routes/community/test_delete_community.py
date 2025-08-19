# Tests
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.tokens import get_access_token


class TestDeleteCommunity(TestRoute):
    route = '/community/{}'

    def test_delete_community(self):
        # Create a community
        community = CommunityFactory()

        # Get the community owner
        owner = community.owner

        # Get owner access token
        access_token = get_access_token(owner)

        # Delete the community
        response = self.DELETERequest(self.route.format(community.name), token=access_token)

        # Rssert the response status code
        self.assertStatusCode(response, 204)

    def test_delete_community_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Delete the community
        response = self.DELETERequest('/community/inexistent', token=access_token)

        # Assert the response status code
        self.assertStatusCode(response, 404)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIn('message', data)

        # Assert the error
        self.assertEqual(data['message'], 'Community not found.')

    def test_delete_community_not_being_owner(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Delete the community
        response = self.DELETERequest(f'/community/{community.name}', token=access_token)

        # Assert response status code
        self.assertStatusCode(response, 403)
        
        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIn('message', data)

        # Assert the error
        self.assertEqual(data['message'], 'You are not the owner of this community.')
