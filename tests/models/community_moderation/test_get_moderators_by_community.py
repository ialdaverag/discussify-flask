# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityModerator

# Flask-SQLAlchemy
from flask_sqlalchemy.pagination import Pagination


class TestGetModerators(BaseTestCase):
    def test_get_moderators(self):
        # Number of moderators
        n = 5
        
        # Create a community
        community = CommunityFactory()

        # Create some moderators
        moderators = UserFactory.create_batch(n)

        # Make the moderators moderators of the community
        for moderator in moderators:
            CommunityModerator(community=community, user=moderator).save()

        # Set args
        args = {}

        # Get the moderators of the community
        moderators_to_read = CommunityModerator.get_moderators_by_community(community, args)

        # Assert moderators_to_read is a Pagination object
        self.assertIsInstance(moderators_to_read, Pagination)

        # Get the items
        moderators_items = moderators_to_read.items

        # Assert the number of moderators
        self.assertEqual(len(moderators_items), n)

        # Assert the moderators are the same
        self.assertEqual(moderators, moderators_items)

    def test_get_moderators_no_moderators(self):
        # Create a community
        community = CommunityFactory()

        # Set args
        args = {}

        # Get the moderators of the community
        moderators = CommunityModerator.get_moderators_by_community(community, args)

        # Assert moderators is a Pagination object
        self.assertIsInstance(moderators, Pagination)

        # Get the items
        moderators_items = moderators.items

        # Assert that there are no moderators
        self.assertEqual(len(moderators_items), 0)

        # Assert that the moderators are an empty list
        self.assertEqual(moderators_items, [])