# Test helper utilities to reduce code duplication

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Block

# Utils
from tests.utils.tokens import get_access_token


class CommonTestMixin:
    """Mixin class providing common test functionality."""
    
    def create_users_batch(self, count):
        """Create multiple users at once."""
        return UserFactory.create_batch(count)
        
    def create_authenticated_user(self):
        """Create a user and return both user and access token."""
        user = UserFactory()
        access_token = get_access_token(user)
        return user, access_token
        
    def make_authenticated_get_request(self, route, user=None, query_string=None):
        """Make a GET request with authentication."""
        if user is None:
            user = UserFactory()
        
        access_token = get_access_token(user)
        headers = {'Authorization': f'Bearer {access_token}'}
        
        if query_string:
            return self.client.get(route, headers=headers, query_string=query_string)
        else:
            return self.client.get(route, headers=headers)
            
    def create_block_relationship(self, blocker, blocked):
        """Create a single block relationship."""
        Block(blocker=blocker, blocked=blocked).save()
        
    def create_multiple_blocks(self, blocker, blocked_users):
        """Create multiple block relationships from one user to many."""
        for blocked_user in blocked_users:
            self.create_block_relationship(blocker, blocked_user)
            
    def create_reverse_blocks(self, blocked_user, blocking_users):
        """Create multiple block relationships from many users to one."""
        for blocking_user in blocking_users:
            self.create_block_relationship(blocking_user, blocked_user)


def setup_pagination_test_data(n_items, create_function, **kwargs):
    """Generic function to setup test data for pagination tests."""
    return create_function(n_items, **kwargs)


def calculate_pagination_values(total_items, page=1, per_page=10):
    """Calculate expected pagination values given total items and pagination parameters."""
    if total_items == 0:
        return {
            'expected_page': page,
            'expected_pages': 0,
            'expected_per_page': per_page,
            'expected_total': 0,
            'expected_count': 0
        }
    
    expected_pages = ((total_items - 1) // per_page) + 1
    start_item = (page - 1) * per_page
    expected_count = min(per_page, max(0, total_items - start_item))
    
    return {
        'expected_page': page,
        'expected_pages': expected_pages,
        'expected_per_page': per_page,
        'expected_total': total_items,
        'expected_count': expected_count
    }