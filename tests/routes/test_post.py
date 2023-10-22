from ..base_test_case import BaseTestCase
from tests.utils.login import login

from app.models.user import User
from app.models.community import Community

from app.extensions.database import db
from app.utils.password import hash_password


class PostTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        user = User(username='test', email='test@example.com', password=hash_password('TestPassword123'))
        user2 = User(username='test2', email='test2@example.com', password=hash_password('TestPassword132'))
        user3 = User(username='test3', email='test3@example.com', password=hash_password('TestPassword132'))

        db.session.add_all([user, user2, user3])
        db.session.commit()
    
        community = user.create_community(name='TestCommunity', about='A community created for tests')
        community2 = user2.create_community(name='TestCommunity2',about='Another community created for tests')

        community.append_subscriber(user2)
        community.append_moderator(user3)
        community2.append_banned(user3)

        post = user2.create_post(
            title='My first post', 
            content='This is my first post in this community', 
            community=community
        )

        post2 = user2.create_post(
            title='A simple test post',
            content='...',
            community=community2
        )

        self.user = user
        self.user2 = user2
        self.user3 = user3
        self.community = community
        self.community2 = community2
        self.post = post
        self.post2 = post2


class CreatePostTests(PostTests):
    def test_create_post(self):
        access_token = login(user=self.user2)
        community_id = self.community.id
        
        route = 'post/'
        content_type='application/json'
        json = {
            'title': 'New Post',
            'content': 'A new post in the community',
            'community_id': community_id
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

    def test_create_post_no_title(self):
        access_token = login(user=self.user2)
        community_id = self.community.id
        
        route = 'post/'
        content_type='application/json'
        json = {
            'content': 'A new post in the community',
            'community_id': community_id
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

    def test_create_post_no_content(self):
        access_token = login(user=self.user2)
        community_id = self.community.id
        
        route = 'post/'
        content_type='application/json'
        json = {
            'title': 'New Post',
            'community_id': community_id
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

    def test_create_post_no_community_id(self):
        access_token = login(user=self.user2)
        community_id = self.community.id
        
        route = 'post/'
        content_type='application/json'
        json = {
            'title': 'New Post',
            'content': 'A new post in the community'
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

    def test_create_post_incorrect_title(self):
        access_token = login(user=self.user2)
        community_id = self.community.id
        
        route = 'post/'
        content_type='application/json'
        json = {
            'title': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed diam metus, varius eget porta at, tincidunt ac dui.',
            'content': 'A new post in the community',
            'community_id': community_id
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

    def test_create_post_incorrect_content(self):
        access_token = login(user=self.user2)
        community_id = self.community.id
        
        route = 'post/'
        content_type='application/json'
        json = {
            'title': 'New Post',
            'content': '',
            'community_id': community_id
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

    def test_create_post_community_not_found(self):
        access_token = login(user=self.user2)
        community_id = 999
        
        route = 'post/'
        content_type='application/json'
        json = {
            'title': 'New Post',
            'content': 'A new post in the community',
            'community_id': community_id
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

        self.assertEqual(404, response.status_code)

    def test_create_post_not_subscribed(self):
        access_token = login(user=self.user)
        community_id = self.community2.id
        
        route = 'post/'
        content_type='application/json'
        json = {
            'title': 'New Post',
            'content': 'A new post in the community',
            'community_id': community_id
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

    def test_create_post_banned_user(self):
        access_token = login(user=self.user3)
        community_id = self.community2.id
        
        route = 'post/'
        content_type='application/json'
        json = {
            'title': 'New Post',
            'content': 'A new post in the community',
            'community_id': community_id
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

    
class UpdatePostTests(PostTests):
    def test_update_post(self):
        access_token = login(user=self.user2)
        post = self.post
        
        route = f'post/{post.id}'
        content_type='application/json'
        json = {
            'title': 'My first updated Post',
            'content': 'A updated post in the community'
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

    def test_update_non_existent_post(self):
        access_token = login(user=self.user2)
        post = 999
        
        route = f'post/{post}'
        content_type='application/json'
        json = {
            'title': 'My first updated Post',
            'content': 'A updated post in the community'
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

        self.assertEqual(404, response.status_code)

    def test_update_post_incorrect_title(self):
        access_token = login(user=self.user2)
        post = self.post
        
        route = f'post/{post.id}'
        content_type='application/json'
        json = {
            'title': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed diam metus, varius eget porta at, tincidunt ac dui.',
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

    def test_update_post_incorrect_content(self):
        access_token = login(user=self.user2)
        post = self.post
        
        route = f'post/{post.id}'
        content_type='application/json'
        json = {
            'content': ''
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

    def test_update_post_not_owner(self):
        access_token = login(user=self.user)
        post = self.post
        
        route = f'post/{post.id}'
        content_type='application/json'
        json = {
            'title': 'My first updated Post',
            'content': 'A updated post in the community'
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

    
class DeletePost(PostTests):
    def test_delete_post_being_owner(self):
        access_token = login(user=self.user2)
        post_id = self.post.id
        
        route = f'post/{post_id}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.delete(
            route,
            headers=headers
        )

        self.assertEqual(204, response.status_code)

    def test_delete_post_being_mod(self):
        access_token = login(user=self.user)
        post_id = self.post.id
        
        route = f'post/{post_id}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.delete(
            route,
            headers=headers
        )

        self.assertEqual(204, response.status_code)


    def test_delete_non_existent_post(self):
        access_token = login(user=self.user2)
        post_id = 999
        
        route = f'post/{post_id}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.delete(
            route,
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_delete_not_being_owner_or_mod(self):
        access_token = login(user=self.user)
        post_id = self.post2.id
        
        route = f'post/{post_id}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.delete(
            route,
            headers=headers
        )

        self.assertEqual(403, response.status_code)

    