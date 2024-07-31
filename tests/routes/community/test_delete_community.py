# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# utils
from tests.utils.tokens import get_access_token


class TestDeleteCommunity(BaseTestCase):
    route = '/community/<string:name>/'

    def test_delete_community(self):
        # create a community
        community = CommunityFactory()

        # create a user
        owner = community.owner

        # get user access token
        access_token = get_access_token(owner)

        # delete the community
        response = self.client.delete(
            f'/community/{community.name}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 204)

    def test_delete_community_nonexistent(self):
        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # delete the community
        response = self.client.delete(
            '/community/inexistent',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)
        # get response data
        data = response.json

        # assert the error
        self.assertEqual(data['message'], 'Community not found.')

    def test_delete_community_not_being_owner(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # delete the community
        response = self.client.delete(
            f'/community/{community.name}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 403)
        
        # get response data
        data = response.json

        # assert the error
        self.assertEqual(data['message'], 'You are not the owner of this community.')
