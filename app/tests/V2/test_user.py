import json
import unittest

from ... import create_app
from ...database_config import destroydb, init_test_db


class TestUser(unittest.TestCase):
    """docstring for TestUser"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            self.db = init_test_db()
        self.data = {
            "name": "Abraham Ogol",
            "username": "aogoll",
            "email": "a@aaaa.com",
            "password": "mcogol"
        }

    def register(self, path="/api/v2/auth/register", data={}):
        destroydb()
        if not data:
            data = self.data
        res = self.client.post(path=path, data=json.dumps(data), headers={"content-type": "application/json"})
        return res

    def test_user_registration(self):
        res = self.register()
        self.assertEqual(res.status_code, 201)

    def test_user_login(self):
        regis = self.register()
        res = self.client.post(path="/api/v2/auth/login", data=json.dumps(self.data), headers={"content-type": "application/json"})
        self.assertEqual(res.status_code, 200)

    def test_login_unexisting_user(self):
        data = {
            "username": "MDASD",
            "password": "ASDASDASDAS"
        }
        res = self.client.post(path="/api/v2/auth/login", data=json.dumps(data), headers={"content-type": "application/json"})
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json['msg'], "No such user")

    def test_unmatching_creds(self):
        regis = self.register()
        data = {
            "username": "aogoll",
            "password": "ASDASDASDAS"
        }
        res = self.client.post(path="/api/v2/auth/login", data=json.dumps(data), headers={"content-type": "application/json"})
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json['msg'], "Username and password does not macth")

    def teaDown(self):
        with self.app.app_context():
            destroydb()
            self.db.close()
