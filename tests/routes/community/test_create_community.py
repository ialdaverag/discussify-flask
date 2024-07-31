# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# utils
from tests.utils.tokens import get_access_token


class TestCreateCommunity(BaseTestCase):
    route = '/community/'

    def test_create_community(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Daa to be sent
        json = {
            'name': 'Videogames',
            'about': 'Community for videogame lovers.',
        }

        # Create a community
        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert that the response status code is 201
        self.assertEqual(response.status_code, 201)

        # Get response data
        data = response.json

        # Assert that the response data is a dictionary
        self.assertIsInstance(data, dict)

        # Assert that the response data contains the community data
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('about', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

        # Assert that the community data is correct
        self.assertEqual(data['name'], 'Videogames')
        self.assertEqual(data['about'], 'Community for videogame lovers.')

        # Assert that the community owner is the user
        self.assertEqual(data['owner']['id'], user.id)

        # Assert stats data
        stats_data = data['stats']
        self.assertIn('id', stats_data)
        self.assertIn('subscribers_count', stats_data)
        self.assertIn('moderators_count', stats_data)
        self.assertIn('banned_count', stats_data)
        self.assertIn('posts_count', stats_data)
        self.assertIn('comments_count', stats_data)

        # Assert that the stats data is correct
        self.assertEqual(stats_data['subscribers_count'], 1)
        self.assertEqual(stats_data['moderators_count'], 1)
        self.assertEqual(stats_data['banned_count'], 0)
        self.assertEqual(stats_data['posts_count'], 0)
        self.assertEqual(stats_data['comments_count'], 0)

    def test_create_community_missing_name(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'about': 'Community for videogame lovers.',
        }

        # Create a community
        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert that the response status code is 400
        self.assertEqual(response.status_code, 400)

        # assert response data
        data = response.json

        self.assertIn('errors', data)
        errors = data['errors']

        # assert errors structure
        self.assertIn('name', errors)

        # assert errors values
        self.assertEqual(errors['name'], ['Missing data for required field.'])

    def test_create_community_invalid_name(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'name': 'Vi',
            'about': 'Community for videogame lovers.',
        }

        # Create a community
        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert that the response status code is 400
        self.assertEqual(response.status_code, 400)

        # assert response data
        data = response.json

        self.assertIn('errors', data)
        errors = data['errors']

        # assert errors structure
        self.assertIn('name', errors)

        # assert errors values
        self.assertEqual(errors['name'], ['Name must be between 3 and 20 characters.'])

    def test_create_community_invalid_about(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'name': 'Videogames',
            'about': 'Community for videogame lovers.' * 100,
        }

        # Create a community
        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert that the response status code is 400
        self.assertEqual(response.status_code, 400)

        # assert response data
        data = response.json

        self.assertIn('errors', data)
        errors = data['errors']

        # assert errors structure
        self.assertIn('about', errors)

        # assert errors values
        self.assertEqual(errors['about'], ['Maximum 1000 characters.'])

    def test_create_community_already_existent_name(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'name': community.name,
            'about': 'Random description.',
        }

        # Create a community
        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert that the response status code is 400
        self.assertEqual(response.status_code, 400)

       # assert response data
        data = response.json

        # assert response structure
        self.assertIn('message', data)

        # assert response data values
        self.assertEqual(data['message'], 'Name already taken.')