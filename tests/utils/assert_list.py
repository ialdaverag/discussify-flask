def assert_user_list(self, users, expected_count=0):
    # Assert that the users is a list
    self.assertIsInstance(users, list)

    # Assert that the length of the users is equal to the expected count
    self.assertEqual(len(users), expected_count)

    # Assert each user in the users list has the expected structure
    for user in users:
        self.assertIn('id', user)
        self.assertIn('username', user)
        self.assertIn('email', user)
        self.assertIn('following', user)
        self.assertIn('follower', user)
        self.assertIn('stats', user)
        self.assertIn('created_at', user)
        self.assertIn('updated_at', user)

def assert_community_list(self, communities, expected_count=0):
    # Assert that the communities is a list
    self.assertIsInstance(communities, list)

    # Assert that the length of the communities is equal to the expected count
    self.assertEqual(len(communities), expected_count)

    # Assert each community in the communities list has the expected structure
    for community in communities:
        self.assertIn('id', community)
        self.assertIn('name', community)
        self.assertIn('about', community)
        self.assertIn('owner', community)
        self.assertIn('owned_by', community)
        self.assertIn('subscriber', community)
        self.assertIn('moderator', community)
        self.assertIn('ban', community)
        self.assertIn('stats', community)
        self.assertIn('created_at', community)
        self.assertIn('updated_at', community)


def assert_post_list(self, posts, expected_count=0):
    # Assert that the posts is a list
    self.assertIsInstance(posts, list)

    # Assert that the length of the posts is equal to the expected count
    self.assertEqual(len(posts), expected_count)

    # Assert each post in the posts list has the expected structure
    for post in posts:
        self.assertIn('id', post)
        self.assertIn('title', post)
        self.assertIn('content', post)
        self.assertIn('owner', post)
        self.assertIn('community', post)
        self.assertIn('bookmarked', post)
        self.assertIn('upvoted', post)
        self.assertIn('downvoted', post)
        self.assertIn('stats', post)
        self.assertIn('created_at', post)
        self.assertIn('updated_at', post)

def assert_comment_list(self, comments, expected_count=0):
    # Assert that the comments is a list
    self.assertIsInstance(comments, list)

    # Assert that the length of the comments is equal to the expected count
    self.assertEqual(len(comments), expected_count)

    # Assert each comment in the comments list has the expected structure
    for comment in comments:
        self.assertIn('id', comment)
        self.assertIn('content', comment)
        self.assertIn('owner', comment)
        self.assertIn('post', comment)
        self.assertIn('bookmarked', comment)
        self.assertIn('upvoted', comment)
        self.assertIn('downvoted', comment)
        self.assertIn('replies', comment)
        self.assertIn('stats', comment)
        self.assertIn('created_at', comment)
        self.assertIn('updated_at', comment)