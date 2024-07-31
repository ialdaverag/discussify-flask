# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# utils
from tests.utils.tokens import get_access_token


class TestUpdateCommunity(BaseTestCase):
    route = '/community/<string:name>/'

    def test_update_community(self):
        # create a community
        community = CommunityFactory()

        # create a user
        owner = community.owner

        # get user access token
        access_token = get_access_token(owner)

        # data to be sent
        json = {
            'name': 'Videogames',
            'about': 'Community for videogame lovers.',
        }

        # update the community
        response = self.client.patch(
            f'/community/{community.name}',
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # assert response status code
        self.assertEqual(response.status_code, 200)

        # get response data
        data = response.json

        # assert the community
        self.assertEqual(data['id'], community.id)
        self.assertEqual(data['name'], 'Videogames')
        self.assertEqual(data['about'], 'Community for videogame lovers.')

    def test_update_community_nonexistent(self):
        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # data to be sent
        json = {
            'name': 'Videogames',
            'about': 'Community for videogame lovers.',
        }

        # update the community
        response = self.client.patch(
            '/community/inexistent',
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)

        # get response data
        data = response.json

        # assert the error
        self.assertEqual(data['message'], 'Community not found.')

    def test_update_community_not_being_owner(self):
        # create a community
        community = CommunityFactory()

        # create a user
        user = UserFactory()

        # get user access token
        access_token = get_access_token(user)

        # data to be sent
        json = {
            'name': 'Videogames',
            'about': 'Community for videogame lovers.',
        }

        # update the community
        response = self.client.patch(
            f'/community/{community.name}',
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # assert response status code
        self.assertEqual(response.status_code, 403)

        # get response data
        data = response.json

        # assert the error
        self.assertEqual(data['message'], 'You are not the owner of this community.')

    def test_update_community_invalid_name(self):
        # create a community
        community = CommunityFactory()

        # create a user
        owner = community.owner

        # get user access token
        access_token = get_access_token(owner)

        # data to be sent
        json = {
            'name': 'Invalid Name',
            'about': 'Community for videogame lovers.',
        }

        # update the community
        response = self.client.patch(
            f'/community/{community.name}',
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

        # get response data
        data = response.json

        self.assertIn('errors', data)
        errors = data['errors']

        # assert errors structure
        self.assertIn('name', errors)

        # assert errors values
        self.assertEqual(errors['name'], ['Name must consist of letters, numbers, and underscores only.'])

    def test_update_community_invalid_about(self):
        # create a community
        community = CommunityFactory()

        # create a user
        owner = community.owner

        # get user access token
        access_token = get_access_token(owner)

        # data to be sent
        json = {
            'name': 'Videogames',
            'about': 'Community for videogame lovers.' * 100,
        }

        # update the community
        response = self.client.patch(
            f'/community/{community.name}',
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

        # get response data
        data = response.json

        self.assertIn('errors', data)
        errors = data['errors']

        # assert errors structure
        self.assertIn('about', errors)

        # assert errors values
        self.assertEqual(errors['about'], ['Maximum 1000 characters.'])
        

    def test_update_community_already_existent_name(self):
        # create a community
        community1 = CommunityFactory()
        community2 = CommunityFactory()

        # get owner
        owner = community2.owner

        # get user access token
        access_token = get_access_token(owner)

        # data to be sent
        json = {
            'name': community1.name,
            'about': 'Random description.',
        }

        # update the community
        response = self.client.patch(
            f'/community/{community2.name}',
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

        # get response data
        data = response.json

        # assert the error
        self.assertEqual(data['message'], 'Name already taken.')