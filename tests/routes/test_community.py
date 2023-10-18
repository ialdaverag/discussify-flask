from ..base_test_case import BaseTestCase
from tests.utils.login import login

from app.models.user import User
from app.models.community import Community

from app.extensions.database import db
from app.utils.password import hash_password


class CommunityTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        user = User(
            username='test', 
            email='test@example.com', 
            password=hash_password('TestPassword123')
        )
        db.session.add(user)
        db.session.commit()

        community = Community(
            name='TestCommunity',
            about='A community created for tests'
        )
        db.session.add(community)
        db.session.commit()

        self.user = user


class CreateCommunityTests(CommunityTests):
    def test_create_community(self):
        access_token = login(user=self.user)
        
        route = 'community/'
        content_type='application/json'
        json = {
            'name': 'TestCommunity2',
            'about': 'A new community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(201, response.status_code)

    def test_create_community_no_name(self):
        access_token = login(user=self.user)
        
        route = 'community/'
        content_type='application/json'
        json = {
            'about': 'A new community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(400, response.status_code)

    def test_create_community_name_taken(self):
        access_token = login(user=self.user)
        
        route = 'community/'
        content_type='application/json'
        json = {
            'name': 'TestCommunity',
            'about': 'A new community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(400, response.status_code)

    def test_create_community_incorrect_name(self):
        access_token = login(user=self.user)
        
        route = 'community/'
        content_type='application/json'
        json = {
            'name': 'Test Community',
            'about': 'A new community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(400, response.status_code)