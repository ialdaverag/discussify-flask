from ..base_test_case import BaseTestCase
from tests.utils.login import login

from app.models.user import User
from app.models.community import Community

from app.extensions.database import db
from app.utils.password import hash_password


class CommunityTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        user = User(username='test', email='test@example.com', password=hash_password('TestPassword123'))
        community = Community(name='TestCommunity', about='A community created for tests', owner=user)
        user2 = User(username='test2', email='test2@example.com', password=hash_password('TestPassword132'))
        community2 = Community(name='TestCommunity2',about='Another community created for tests', owner=user2)

        db.session.add_all([user, community, user2, community2])
        db.session.commit()

        self.user = user
        self.community = community
        self.user2 = user2
        self.community2 = community2


class CreateCommunityTests(CommunityTests):
    def test_create_community(self):
        access_token = login(user=self.user)
        
        route = 'community/'
        content_type='application/json'
        json = {
            'name': 'NewCommunity',
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

class UpdateCommunityTests(CommunityTests):
    def test_update_community(self):
        access_token = login(user=self.user)
        community = self.community.name
        
        route = f'community/{community}'
        content_type='application/json'
        json = {
            'name': 'UpdatedCommunity',
            'about': 'A updated community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.patch(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(200, response.status_code)

    def test_update_community_incorrect_owner(self):
        access_token = login(user=self.user2)
        community = self.community.name

        route = f'community/{community}'
        content_type='application/json'
        json = {
            'name': 'UpdatedCommunity',
            'about': 'A updated community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.patch(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(403, response.status_code)

    def test_update_community_incorrect_name(self):
        access_token = login(user=self.user)
        community = self.community.name
        
        route = f'community/{community}'
        content_type='application/json'
        json = {
            'name': 'Updated Community',
            'about': 'A updated community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.patch(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(400, response.status_code)
    
    def test_update_community_name_taken(self):
        access_token = login(user=self.user2)
        
        route = f'community/{self.community2.name}'
        content_type='application/json'
        json = {
            'name': 'TestCommunity',
            'about': 'A new community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.patch(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(400, response.status_code)
    