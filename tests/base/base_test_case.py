# tests/base/base_test_case.py
import unittest
from app.app import create_app
from app.config.testing import TestingConfig
from app.extensions.database import db

class BaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create all tables
        db.create_all()
        
        # Create test client
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        # Close all sessions and connections
        db.session.remove()
        db.drop_all()
        
        # Dispose of the engine to close all connections
        db.engine.dispose()
        
        # Pop app context
        self.app_context.pop()