import unittest

from app.app import create_app
from app.extensions.database import db
from app.config.testing import TestingConfig


class BaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # create the app with testing config
        self.app = create_app(TestingConfig)

        # create and add the app context
        self.app_context = self.app.app_context()
        self.app_context.push()

        # create the database tables
        db.create_all()

        # create the app test client
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        # close the database session
        db.session.close()

        # delete the database tables
        db.drop_all()

        # remove the app context
        self.app_context.pop()