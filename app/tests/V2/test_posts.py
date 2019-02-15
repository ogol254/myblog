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
            "title": "Test  3 ",
            "description": "Lorem ",
            "created_by": 4
        }

    def register_user(self, path="/api/v2/auth/register", data={}):
        destroydb()
        if not data:
            data = {
                "name": "Abraham Ogol",
                "username": "aogoll",
                "email": "a@aaaa.com",
                "password": "mcogol"
            }
        header = {"content-type": "application/json"}
        res = self.client.post(path=path, data=json.dumps(data), headers=header)
        return res.json['access-token']

    def post(self, path="/api/v2/blog", data={}):
        if not data:
            data = self.data
        token = self.register_user()
        header = {
            "Authorization": "Bearer {}".format(token),
            "content-type": "application/json"
        }
        res = self.client.post(path=path, data=json.dumps(data), headers=header)
        return res

    def get(self, path="/api/v2/blog", data={}):
        token = self.register_user()
        header = {
            "Authorization": "Bearer {}".format(token),
            "content-type": "application/json"
        }
        res = self.client.get(path=path, headers=header)
        return res

    def test_posting_blog(self):
        res = self.post()
        self.assertEqual(res.status_code, 201)

    def test_getting_blog(self):
        res = self.get()
        self.assertEqual(res.status_code, 200)
