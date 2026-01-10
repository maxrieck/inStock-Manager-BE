from app import create_app
from application.models import db
import unittest


class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()


    def test_create_user(self):
        user_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "jonh@test.com",
            "password": "1234",
            "role_id": 1
        }
        response = self.client.post('/users/', json=user_payload)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json['first_name'], "John")