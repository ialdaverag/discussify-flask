# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# utils
from tests.utils.tokens import get_access_token


class TestReadCommunities(BaseTestCase):
    route = '/community/'

    def test_read_community(self):
        # create multiple communities
        communities = CommunityFactory.create_batch(size=5)

        # get the communities
        response = self.client.get(self.route)

        # assert response status code
        self.assertEqual(response.status_code, 200)

        # get response data
        data = response.json

        # assert the number of communities
        self.assertEqual(len(data), len(communities))

        # assert each community
        for i, community in enumerate(communities):
            self.assertEqual(data[i]['id'], community.id)
            self.assertEqual(data[i]['name'], community.name)
            self.assertEqual(data[i]['about'], community.about)
            self.assertEqual(data[i]['created_at'], community.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
            self.assertEqual(data[i]['updated_at'], community.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_read_community_empty(self):
        # get the communities
        response = self.client.get(self.route)

        # assert response status code
        self.assertEqual(response.status_code, 200)

        # get response data
        data = response.json

        # assert the community
        self.assertEqual(len(data), 0)
