# Base
from tests.routes.test_route import TestRoute

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.post_factory import PostFactory

# Utils
from tests.utils.tokens import get_access_token


class TestUpdatePost(TestRoute):
    route = '/post/{}'

    def test_update_post(self):
        # Create a post
        post = PostFactory()

        # Get the owner of the post
        owner = post.owner

        # Data to be sent
        json = {
            'title': 'New title',
            'content': 'New content',
        }

        # Get the access token
        access_token = get_access_token(owner)

        # Update the post
        response = self.PATCHRequest(
            self.route.format(post.id),
            token=access_token,
            data=json
        )

        # Check status code
        self.assertStatusCode(response, 200)

        # Get the data
        data = response.json

        # Assert keys in data
        self.assertIn('id', data)
        self.assertIn('title', data)
        self.assertIn('content', data)
        self.assertIn('owner', data)
        self.assertIn('community', data)
        self.assertIn('bookmarked', data)
        self.assertIn('upvoted', data)
        self.assertIn('downvoted', data)
        self.assertIn('stats', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

        # Assert that the community data is correct
        self.assertEqual(data['title'], json['title'])
        self.assertEqual(data['content'], json['content'])
        self.assertEqual(data['community']['id'], post.community.id)
        self.assertEqual(data['owner']['id'], owner.id)

        # # Get the stats data from the response
        stats_data = data['stats']

        # Assert the stats data
        self.assertIn('id', stats_data)
        self.assertIn('comments_count', stats_data)
        self.assertIn('bookmarks_count', stats_data)
        self.assertIn('upvotes_count', stats_data)
        self.assertIn('downvotes_count', stats_data)

        # Assert the stats data values
        self.assertEqual(stats_data['comments_count'], 0)
        self.assertEqual(stats_data['bookmarks_count'], 0)
        self.assertEqual(stats_data['upvotes_count'], 0)
        self.assertEqual(stats_data['downvotes_count'], 0)

    def test_update_post_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Data to be sent
        json = {
            'title': 'New title',
            'content': 'New content',
            'community_id': 1
        }

        # Get the access token
        access_token = get_access_token(user)

        # Update the post
        response = self.PATCHRequest(self.route.format(404),
            json=json,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert status code
        self.assertEqual(response.status_code, 404)

        # Get the response data
        data = response.json

        # Assert keys in response data
        self.assertIn('message', data)

        # Assert response data values
        self.assertEqual(data['message'], 'Post not found.')

    def test_update_post_invalid_title(self):
        # Create a post
        post = PostFactory()

        # Get the owner of the post
        owner = post.owner

        # Data to be sent
        json = {
            'title': 'a',
            'content': 'New content',
        }

        # Get the access token
        access_token = get_access_token(owner)

        # Update the post
        response = self.PATCHRequest(self.route.format(post.id),
            json=json,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

       # Get the data
        data = response.json

        # Get errors from the response data
        errors = data['errors']

        # Assert keys in errors
        self.assertIn('title', errors)

        # Assert errors values
        self.assertEqual(errors['title'], ['Title must be between 8 and 40 characters.'])


    def test_update_post_invalid_content(self):
        # Create a post
        post = PostFactory()

        # Get the owner of the post
        owner = post.owner

        # Data to be sent
        json = {
            'title': 'New title',
            'content': '',
        }

        # Get the access token
        access_token = get_access_token(owner)

        # Update the post
        response = self.PATCHRequest(self.route.format(post.id),
            json=json,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 400)

       # Get the data
        data = response.json

        # Get errors from the response data
        errors = data['errors']

        # Assert keys in errors
        self.assertIn('content', errors)

        # Assert errors values
        self.assertEqual(errors['content'], ['Content must contain at least 1 character.'])

    def test_update_post_not_being_owner(self):
        # Create a post
        post = PostFactory()

        # Create a user
        user = UserFactory()

        # Data to be sent
        json = {
            'community_id': post.community.id,
            'title': 'New title',
            'content': 'New content'
        }

        # Get the access token
        access_token = get_access_token(user)

        # Update the post
        response = self.PATCHRequest(self.route.format(post.id),
            json=json,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Check status code
        self.assertEqual(response.status_code, 403)

        # Get the data
        data = response.json

        # Assert keys in data
        self.assertIn('message', data)

        # Assert response data values
        self.assertEqual(data['message'], 'You are not the owner of this post.')
