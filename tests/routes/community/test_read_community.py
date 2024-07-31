# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# utils
from tests.utils.tokens import get_access_token


class TestReadCommunity(BaseTestCase):
    route = '/community/<string:name>/'

    def test_read_community(self):
        # create a community
        community = CommunityFactory()

        # get the community
        response = self.client.get(f'/community/{community.name}')

        # assert response status code
        self.assertEqual(response.status_code, 200)

        # get response data
        data = response.json

        # assert the community
        self.assertEqual(data['id'], community.id)
        self.assertEqual(data['name'], community.name)
        self.assertEqual(data['about'], community.about)
        self.assertEqual(data['created_at'], community.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(data['updated_at'], community.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_read_community_not_found(self):
        # get the community
        response = self.client.get('/community/inexistent')

        # assert response status code
        self.assertEqual(response.status_code, 404)

        # get response data
        data = response.json

        # assert the error
        self.assertEqual(data['message'], 'Community not found.')