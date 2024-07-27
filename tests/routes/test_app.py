# Flask
from flask import current_app

# tests
from tests.base.base_test_case import BaseTestCase


class TestApp(BaseTestCase):
    def test_app(self) -> None:
        assert self.app is not None
        assert current_app == self.app
