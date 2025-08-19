def assert_list_structure(self, items, expected_count=0, required_fields=None):
    """
    Generic function to assert list structure and item fields.
    
    Args:
        self: Test case instance
        items: List to validate
        expected_count: Expected number of items in the list
        required_fields: List of field names that each item must contain
    """
    # Assert that the items is a list
    self.assertIsInstance(items, list)

    # Assert that the length of the items is equal to the expected count
    self.assertEqual(len(items), expected_count)

    # Assert each item in the list has the expected structure
    if required_fields:
        for item in items:
            for field in required_fields:
                self.assertIn(field, item)


def assert_user_list(self, users, expected_count=0):
    """Assert structure and count of a user list."""
    required_fields = [
        'id', 'username', 'email', 'following', 'follower', 
        'stats', 'created_at', 'updated_at'
    ]
    assert_list_structure(self, users, expected_count, required_fields)


def assert_community_list(self, communities, expected_count=0):
    """Assert structure and count of a community list."""
    required_fields = [
        'id', 'name', 'about', 'owner', 'owned_by', 'subscriber', 
        'moderator', 'ban', 'stats', 'created_at', 'updated_at'
    ]
    assert_list_structure(self, communities, expected_count, required_fields)


def assert_post_list(self, posts, expected_count=0):
    """Assert structure and count of a post list."""
    required_fields = [
        'id', 'title', 'content', 'owner', 'community', 'bookmarked', 
        'upvoted', 'downvoted', 'stats', 'created_at', 'updated_at'
    ]
    assert_list_structure(self, posts, expected_count, required_fields)


def assert_comment_list(self, comments, expected_count=0):
    """Assert structure and count of a comment list."""
    required_fields = [
        'id', 'content', 'owner', 'post', 'bookmarked', 'upvoted', 
        'downvoted', 'replies', 'stats', 'created_at', 'updated_at'
    ]
    assert_list_structure(self, comments, expected_count, required_fields)