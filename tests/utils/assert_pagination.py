def assert_pagination_structure(
        self,   
        pagination,
        data_key='users',
        expected_page=1, 
        expected_pages=1, 
        expected_per_page=10, 
        expected_total=10
    ):
    """
    Assert the structure and values of a pagination response.
    
    Args:
        self: Test case instance
        pagination: Pagination response dictionary to validate
        data_key: The key name for the data array (e.g., 'users', 'posts', 'communities', 'comments')
        expected_page: Expected current page number
        expected_pages: Expected total number of pages
        expected_per_page: Expected items per page
        expected_total: Expected total number of items
    """
    # Assert that the pagination is a dictionary
    self.assertIsInstance(pagination, dict)

    # Assert that the pagination has the expected keys
    self.assertIn('links', pagination)
    self.assertIn('page', pagination)
    self.assertIn('pages', pagination)
    self.assertIn('per_page', pagination)
    self.assertIn('total', pagination)
    self.assertIn(data_key, pagination)

    # Assert that the links is a dictionary    
    self.assertIsInstance(pagination['links'], dict)

    # Assert that the links has the expected keys
    self.assertIn('first', pagination['links'])
    self.assertIn('last', pagination['links'])

    # Assert navigation links based on current page
    if expected_page > 1:
        self.assertIn('prev', pagination['links'])
    else:
        self.assertNotIn('prev', pagination['links'])
    
    # Assert next link based on current page and total pages
    if expected_page < expected_pages:
        self.assertIn('next', pagination['links'])
    else:
        self.assertNotIn('next', pagination['links'])

    # Assert the values of the pagination
    self.assertEqual(pagination['page'], expected_page)
    self.assertEqual(pagination['pages'], expected_pages)
    self.assertEqual(pagination['per_page'], expected_per_page)
    self.assertEqual(pagination['total'], expected_total)


# Backward compatibility wrapper functions
def assert_pagination_structure_users(
        self,   
        pagination, 
        expected_page=1, 
        expected_pages=1, 
        expected_per_page=10, 
        expected_total=10
    ):
    """Backward compatibility wrapper for user pagination assertions."""
    return assert_pagination_structure(
        self, pagination, 'users', expected_page, expected_pages, expected_per_page, expected_total
    )


def assert_pagination_structure_communities(
        self,   
        pagination, 
        expected_page=1, 
        expected_pages=1, 
        expected_per_page=10, 
        expected_total=10
    ):
    """Backward compatibility wrapper for community pagination assertions."""
    return assert_pagination_structure(
        self, pagination, 'communities', expected_page, expected_pages, expected_per_page, expected_total
    )


def assert_pagination_structure_posts(
        self,   
        pagination, 
        expected_page=1, 
        expected_pages=1, 
        expected_per_page=10, 
        expected_total=10
    ):
    """Backward compatibility wrapper for post pagination assertions."""
    return assert_pagination_structure(
        self, pagination, 'posts', expected_page, expected_pages, expected_per_page, expected_total
    )


def assert_pagination_structure_comments(
        self,   
        pagination, 
        expected_page=1, 
        expected_pages=1, 
        expected_per_page=10, 
        expected_total=10
    ):
    """Backward compatibility wrapper for comment pagination assertions."""
    return assert_pagination_structure(
        self, pagination, 'comments', expected_page, expected_pages, expected_per_page, expected_total
    )