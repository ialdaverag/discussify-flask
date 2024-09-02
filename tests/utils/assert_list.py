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