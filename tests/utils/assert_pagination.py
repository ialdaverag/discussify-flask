def assert_pagination_structure(
        self,   
        pagination, 
        expected_page=1, 
        expected_pages=1, 
        expected_per_page=10, 
        expected_total=10
    ):
    
    # Assert that the pagination is a dictionary
    self.assertIsInstance(pagination, dict)

    # Assert that the pagination has the expected keys
    self.assertIn('links', pagination)
    self.assertIn('page', pagination)
    self.assertIn('pages', pagination)
    self.assertIn('per_page', pagination)
    self.assertIn('total', pagination)
    self.assertIn('users', pagination)

    # Assert that the links is a dictionary    
    self.assertIsInstance(pagination['links'], dict)

    # Assert that the links has the expected keys
    self.assertIn('first', pagination['links'])
    self.assertIn('last', pagination['links'])

    # Assert 
    if expected_page > 1:
        self.assertIn('prev', pagination['links'])
    else:
        self.assertNotIn('prev', pagination['links'])
    
    # Assert 
    if expected_page < expected_pages:
        self.assertIn('next', pagination['links'])
    else:
        self.assertNotIn('next', pagination['links'])

    # Assert the values of the pagination
    self.assertEqual(pagination['page'], expected_page)
    self.assertEqual(pagination['pages'], expected_pages)
    self.assertEqual(pagination['per_page'], expected_per_page)
    self.assertEqual(pagination['total'], expected_total)


def assert_pagination_structure_communities(
        self,   
        pagination, 
        expected_page=1, 
        expected_pages=1, 
        expected_per_page=10, 
        expected_total=10
    ):
    
    # Assert that the pagination is a dictionary
    self.assertIsInstance(pagination, dict)

    # Assert that the pagination has the expected keys
    self.assertIn('links', pagination)
    self.assertIn('page', pagination)
    self.assertIn('pages', pagination)
    self.assertIn('per_page', pagination)
    self.assertIn('total', pagination)
    self.assertIn('communities', pagination)

    # Assert that the links is a dictionary    
    self.assertIsInstance(pagination['links'], dict)

    # Assert that the links has the expected keys
    self.assertIn('first', pagination['links'])
    self.assertIn('last', pagination['links'])

    # Assert 
    if expected_page > 1:
        self.assertIn('prev', pagination['links'])
    else:
        self.assertNotIn('prev', pagination['links'])
    
    # Assert 
    if expected_page < expected_pages:
        self.assertIn('next', pagination['links'])
    else:
        self.assertNotIn('next', pagination['links'])

    # Assert the values of the pagination
    self.assertEqual(pagination['page'], expected_page)
    self.assertEqual(pagination['pages'], expected_pages)
    self.assertEqual(pagination['per_page'], expected_per_page)
    self.assertEqual(pagination['total'], expected_total)


def assert_pagination_structure_posts(
        self,   
        pagination, 
        expected_page=1, 
        expected_pages=1, 
        expected_per_page=10, 
        expected_total=10
    ):
    
    # Assert that the pagination is a dictionary
    self.assertIsInstance(pagination, dict)

    # Assert that the pagination has the expected keys
    self.assertIn('links', pagination)
    self.assertIn('page', pagination)
    self.assertIn('pages', pagination)
    self.assertIn('per_page', pagination)
    self.assertIn('total', pagination)
    self.assertIn('posts', pagination)

    # Assert that the links is a dictionary    
    self.assertIsInstance(pagination['links'], dict)

    # Assert that the links has the expected keys
    self.assertIn('first', pagination['links'])
    self.assertIn('last', pagination['links'])

    # Assert 
    if expected_page > 1:
        self.assertIn('prev', pagination['links'])
    else:
        self.assertNotIn('prev', pagination['links'])
    
    # Assert 
    if expected_page < expected_pages:
        self.assertIn('next', pagination['links'])
    else:
        self.assertNotIn('next', pagination['links'])

    # Assert the values of the pagination
    self.assertEqual(pagination['page'], expected_page)
    self.assertEqual(pagination['pages'], expected_pages)
    self.assertEqual(pagination['per_page'], expected_per_page)
    self.assertEqual(pagination['total'], expected_total)