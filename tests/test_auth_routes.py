from .base_test_case import BaseTestCase
from .create_users import create_users

from app.models.user import User


class AuthTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        create_users()

        print('auth...')


class SignUpTests(AuthTests):    
    def test_sign_up(self):
        response = self.client.post(
            '/auth/signup', 
            content_type='application/json',
            json={
                'username': 'user',
                'email': 'user@example.com',
                'password': 'UserPassword123'
            }
        )

        self.assertEqual(201, response.status_code)
        self.assertEqual('application/json', response.content_type)
        
        self.assertIn('id', response.json)
        self.assertIn('username', response.json)
        self.assertIn('email', response.json)
        self.assertIn('created_at', response.json)
        self.assertIn('updated_at', response.json)

        self.assertEqual('user', response.json['username'])
        self.assertEqual('user@example.com', response.json['email'])

        user = User.query.filter_by(username='user').first()
        self.assertIsNotNone(user)

    def test_sign_up_duplicate_username(self):
        response = self.client.post(
            '/auth/signup', 
            content_type='application/json',
            json={
                'username': 'test',
                'email': 'user2@example.com',
                'password': 'UserPassword321'
            }
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual('application/json', response.content_type)

        self.assertIn('message', response.json)
        self.assertEqual('Username already used', response.json['message'])

        user = User.query.filter_by(username='user').first()
        self.assertIsNone(user)

    def test_sign_up_duplicate_email(self):
        response = self.client.post(
            '/auth/signup', 
            content_type='application/json',
            json={
                'username': 'test2',
                'email': 'test@example.com',
                'password': 'UserPassword231'
            }
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual('application/json', response.content_type)

        self.assertIn('message', response.json)
        self.assertEqual('Email already used', response.json['message'])

        user = User.query.filter_by(username='user').first()
        self.assertIsNone(user)

    def test_sign_up_no_username(self):
        response = self.client.post(
            '/auth/signup',
            content_type='application/json',
            json={
                'email': 'user@example.com',
                'password': 'TestPassword123'
            }
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual('application/json', response.content_type)

        self.assertIn('errors', response.json)
        self.assertIn('username', response.json['errors'])

        self.assertEqual(
            'Missing data for required field.',
            response.json['errors']['username'][0]
        )

        user = User.query.filter_by(email='user@example.com').first()
        self.assertIsNone(user)
    
    def test_sign_up_no_email(self):
        response = self.client.post(
            '/auth/signup', 
            content_type='application/json',
            json={
                'username': 'user',
                'password': 'TestPassword123'
            }
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual('application/json', response.content_type)

        self.assertIn('errors', response.json)
        self.assertIn('email', response.json['errors'])

        self.assertEqual(
            'Missing data for required field.', 
            response.json['errors']['email'][0]
        )

        user = User.query.filter_by(username='user').first()
        self.assertIsNone(user)

    def test_sign_up_no_password(self):
        response = self.client.post(
            '/auth/signup', 
            content_type='application/json',
            json={
                'username': 'user',
                'email': 'user@example.com',
            }
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual('application/json', response.content_type)

        self.assertIn('errors', response.json)
        self.assertIn('password', response.json['errors'])

        self.assertEqual(
            'Missing data for required field.', 
            response.json['errors']['password'][0]
        )

        user = User.query.filter_by(username='user').first()
        self.assertIsNone(user)

    def test_sign_up_invalid_username(self):
        response = self.client.post(
            '/auth/signup',
            content_type='application/json',
            json={
                'username': 'u',
                'email': 'user@example.com',
                'password': 'TestPassword123'
            }
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual('application/json', response.content_type)

        self.assertEqual(
            'username must be between 3 and 20 characters',
            response.json['errors']['username'][0]
        )

        user = User.query.filter_by(username='u').first()
        self.assertIsNone(user)

        response = self.client.post(
            '/auth/signup',
            content_type='application/json',
            json={
                'username': 'thisisalongtestusername',
                'email': 'user@example.com',
                'password': 'TestPassword123'
            }
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual('application/json', response.content_type)

        self.assertEqual(
            'username must be between 3 and 20 characters',
            response.json['errors']['username'][0]
        )

        user = User.query.filter_by(username='thisisalongtestusername').first()
        self.assertIsNone(user)

    def test_sign_up_invalid_email(self):
        response = self.client.post(
            '/auth/signup',
            content_type='application/json',
            json={
                'username': 'user',
                'email': 'userexample.com',
                'password': 'TestPassword123'
            }
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual('application/json', response.content_type)

        self.assertEqual(
            'Not a valid email address.',
            response.json['errors']['email'][0]
        )

        user = User.query.filter_by(username='thisisalongtestusername').first()
        self.assertIsNone(user)

    def test_sign_up_invalid_password(self):
        response = self.client.post(
            '/auth/signup',
            content_type='application/json',
            json={
                'username': 'user',
                'email': 'user@example.com',
                'password': 'Pwd123'
            }
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual('application/json', response.content_type)

        self.assertEqual(
            'password must be between 8 and 40 characters',
            response.json['errors']['password'][0]
        )

        user = User.query.filter_by(username='thisisalongtestusername').first()
        self.assertIsNone(user)
