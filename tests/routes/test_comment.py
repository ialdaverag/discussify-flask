from ..base_test_case import BaseTestCase
from tests.utils.login import login

from app.models.user import User
from app.models.community import Community

from app.extensions.database import db
from app.utils.password import hash_password


class CommentTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        user = User(username='test', email='test@example.com', password=hash_password('TestPassword123'))
        user2 = User(username='test2', email='test2@example.com', password=hash_password('TestPassword132'))
        user3 = User(username='test3', email='test3@example.com', password=hash_password('TestPassword213'))
        user4 = User(username='test4', email='test4@example.com', password=hash_password('TestPassword231'))

        db.session.add_all([user, user2, user3, user4])
        db.session.commit()
    
        community = user.create_community(name='TestCommunity', about='A community created for tests')
        community2 = user2.create_community(name='TestCommunity2',about='Another community created for tests')

        community.append_subscriber(user2)
        community.append_subscriber(user3)
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

        comment = user.create_comment(
            content='Nice post!',
            post=post
        )

        comment2 = user2.create_comment(
            content='Awesome post!',
            post=post
        )

        self.user = user
        self.user2 = user2
        self.user3 = user3
        self.user4 = user4
        self.community = community
        self.community2 = community2
        self.post = post
        self.post2 = post2
        self.comment = comment
        self.comment2 = comment2


class CreateCommentTests(CommentTests):
    def test_create_comment(self):
        access_token = login(user=self.user2)
        post_id = self.post.id
        
        route = 'comment/'
        content_type='application/json'
        json = {
            'content': 'Second comment!',
            'post_id': post_id
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

    def test_create_reply_comment(self):
        access_token = login(user=self.user2)
        post_id = self.post.id
        comment_id = self.comment.id
        
        route = 'comment/'
        content_type='application/json'
        json = {
            'content': 'Third comment!',
            'post_id': post_id,
            'comment_id': comment_id
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

    def test_create_comment_incorrect_content(self):
        access_token = login(user=self.user2)
        post_id = self.post.id
        
        route = 'comment/'
        content_type='application/json'
        json = {
            'content': '',
            'post_id': post_id
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

    def test_create_comment_on_non_existent_post(self):
        access_token = login(user=self.user2)
        post_id = 999
        
        route = 'comment/'
        content_type='application/json'
        json = {
            'content': 'Second comment!',
            'post_id': post_id
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

    def test_create_reply_comment_on_non_existent_comment(self):
        access_token = login(user=self.user2)
        post_id = self.post.id
        comment_id = 999
        
        route = 'comment/'
        content_type='application/json'
        json = {
            'content': 'Third comment!',
            'post_id': post_id,
            'comment_id': comment_id
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

    def test_create_comment_being_banned(self):
        access_token = login(user=self.user3)
        post_id = self.post2.id
        
        route = 'comment/'
        content_type='application/json'
        json = {
            'content': 'My first comment!',
            'post_id': post_id
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

    def test_create_comment_being_not_subscribed(self):
        access_token = login(user=self.user4)
        post_id = self.post.id
        
        route = 'comment/'
        content_type='application/json'
        json = {
            'content': 'My first comment!',
            'post_id': post_id
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


class UpdateCommentTests(CommentTests):
    def test_update_comment(self):
        access_token = login(user=self.user)
        comment_id = self.comment.id
        
        route = f'comment/{comment_id}'
        content_type='application/json'
        json = {
            'content': 'An updated comment!'
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

    def test_update_non_existent_comment(self):
        access_token = login(user=self.user)
        comment_id = 999
        
        route = f'comment/{comment_id}'
        content_type='application/json'
        json = {
            'content': 'An updated comment!'
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

    def test_update_comment_not_owner(self):
        access_token = login(user=self.user2)
        comment_id = self.comment.id
        
        route = f'comment/{comment_id}'
        content_type='application/json'
        json = {
            'content': 'An updated comment!'
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

    def test_update_comment_being_banned(self):
        community = self.community
        community.append_banned(self.user2)

        access_token = login(user=self.user2)
        comment_id = self.comment2.id
        
        route = f'comment/{comment_id}'
        content_type='application/json'
        json = {
            'content': 'An updated comment!'
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

    def test_update_comment_incorrect_content(self):
        access_token = login(user=self.user)
        comment_id = self.comment.id
        
        route = f'comment/{comment_id}'
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