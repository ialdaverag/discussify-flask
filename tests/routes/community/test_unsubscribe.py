# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# utils
from tests.utils.tokens import get_access_token


class TestUnsubscribe(BaseTestCase):
    route = '/community/<string:name>/unsubscribe/'

    def test_unsubscribe(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # subscribe user
        community.append_subscriber(user)

        # get user access token
        access_token = get_access_token(user)

        # unsubscribe from the community
        response = self.client.post(
            f'/community/{community.name}/unsubscribe',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 204)

    def test_unsubscribe_nonexistent(self):
        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # unsubscribe from the community
        response = self.client.post(
            '/community/nonexistent/unsubscribe',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)

    def test_unsubscribe_not_subscribed(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # unsubscribe from the community
        response = self.client.post(
            f'/community/{community.name}/unsubscribe',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

        # get response data
        data = response.json

        # assert error message
        self.assertEqual(data['message'], 'You are not subscribed to this community.')