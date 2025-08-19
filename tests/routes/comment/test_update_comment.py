# Base
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.comment_factory import CommentFactory

# Utils
from tests.utils.tokens import get_access_token

# Models
from app.models.community import CommunityBan


class TestUpdateComment(TestRoute):
    route = '/comment/{}'

    def test_update_comment(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        owner = comment.owner
        
        # Get the access token
        access_token = get_access_token(owner)
        
        # Data to be sent
        json = {
            'content': 'Comment updated.',
        }

        # Update the comment
        response = self.PATCHRequest(self.route.format(comment.id), token=access_token, data=json)

        # Check status code
        self.assertEqual(200, response.status_code)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIn('id', data)
        self.assertIn('content', data)
        self.assertIn('owner', data)
        self.assertIn('post', data)
        self.assertIn('stats', data)

        # Assert the data values
        self.assertEqual(data['content'], 'Comment updated.')
        self.assertEqual(data['owner']['id'], owner.id)
        self.assertEqual(data['post']['id'], comment.post.id)

        # # Get the stats data from the response
        stats_data = data['stats']

        # Assert the stats data
        self.assertIn('id', stats_data)
        self.assertIn('bookmarks_count', stats_data)
        self.assertIn('upvotes_count', stats_data)
        self.assertIn('downvotes_count', stats_data)

        # Assert the stats data values
        self.assertEqual(stats_data['bookmarks_count'], 0)
        self.assertEqual(stats_data['upvotes_count'], 0)
        self.assertEqual(stats_data['downvotes_count'], 0)

    def test_update_comment_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get the access token
        access_token = get_access_token(user)
        
        # Data to be sent
        json = {
            'content': 'Comment updated.',
        }

        # Update the comment
        response = self.PATCHRequest(self.route.format(404), token=access_token, data=json)

        # Check status code
        self.assertEqual(404, response.status_code)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Comment not found.')

    def test_update_comment_missing_content(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        owner = comment.owner
        
        # Get the access token
        access_token = get_access_token(owner)
        
        # Data to be sent
        json = {}

        # Update the comment
        response = self.PATCHRequest(self.route.format(comment.id), token=access_token, data=json)

        # Check status code
        self.assertEqual(400, response.status_code)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIn('errors', data)

        # Get errors from the response data
        errors = data['errors']

        # Assert keys in errors
        self.assertIn('content', errors)

        # Assert errors values
        self.assertEqual(errors['content'], ['Missing data for required field.'])


    def test_update_comment_being_banned(self):
        # Create a comment
        comment = CommentFactory()

        # Create a user
        owner = comment.owner
    
        # Append the owner to the post's community banned list
        community = comment.post.community
        CommunityBan(community=community, user=owner).save()

        # Get the access token
        access_token = get_access_token(owner)
        
        # Data to be sent
        json = {
            'content': 'Comment updated.',
        }

        # Update the comment
        response = self.PATCHRequest(self.route.format(comment.id), token=access_token, data=json)

        # Check status code
        self.assertEqual(400, response.status_code)

        # Get the data
        data = response.json

        # Assert message is in data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'You are banned from this community.')
