# Flask
from flask import current_app

# tests
from tests.routes.test_route import TestRoute


class TestApp(TestRoute):
    def test_app(self) -> None:
        assert self.app is not None
        assert current_app == self.app
