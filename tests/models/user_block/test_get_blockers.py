# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import Block


class TestGetBlockers(BaseTestCase):
    def test_get_blockers(self):
        # Number of users to create
        n = 5

        # Create a user
        user = UserFactory()

        # Create a list of users
        users = UserFactory.create_batch(n)

        # 
        for user_ in users:
            Block(blocker=user_, blocked=user).save()

        # Get the blockers
        blockers = Block.get_blockers(user)

        # Assert that blockers is a list
        self.assertIsInstance(blockers, list)

        # Assert the number of blockers
        self.assertEqual(len(blockers), n)

    def test_get_blockers_empty(self):
        # Create a user
        user = UserFactory()

        # Get the blockers
        blockers = Block.get_blockers(user)

        # Assert that blockers is a list
        self.assertIsInstance(blockers, list)

        # Assert that the blockers is an empty list
        self.assertEqual(blockers, [])
