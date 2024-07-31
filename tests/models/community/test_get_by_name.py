#  base
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.community_factory import CommunityFactory

# models
from app.models.community import Community

# errors
from app.errors.errors import NotFoundError


class TestGetById(BaseTestCase):
    def test_get_by_name(self):
        community = CommunityFactory()

        result = Community.get_by_name(community.name)

        self.assertEqual(result.name, community.name)

    def test_get_by_id__not_found(self):
        with self.assertRaises(NotFoundError):
            Community.get_by_name('not_found')