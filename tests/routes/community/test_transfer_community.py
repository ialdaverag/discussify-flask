# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# utils
from tests.utils.tokens import get_access_token


class TestTransferTo(BaseTestCase):
    def test_transfer_to(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # subscribe user
        community.append_subscriber(user)

        # get user access token
        access_token = get_access_token(community.owner)

        # add moderator to the community
        response = self.client.post(
            f'/community/{community.name}/transfer/{user.username}',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # assert response status code
        self.assertEqual(response.status_code, 204)

    