import json
import unittest
from ... import create_app


class TestMyBlogApp(unittest.TestCase):
    """docstring for TestMyBlogApp"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.data = {
            "title": "Religion is all about faith",
            "description": "Some serious and useful content here"
        }
        self.da = {
            "tittle": "UPDATED: Religion is all about faith",
            "description": "UPDATED: Some serious and useful content here"
        }

    def post(self, path='/blog', data={}):
        if not data:
            data = self.data

        resp = self.client.post(path='/api/v1/blog', data=json.dumps(self.data), content_type='application/json')
        return resp

    def test_posting_a_blog(self):
        resp = self.post()
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json['blog_id'])
        self.assertEqual(resp.json['msg'], 'Created')

    def test_getting_all_blogs(self):
        resp = self.client.get(path='/api/v1/blog', content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_getting_a_single_blog(self):
        post = self.post()
        int_id = int(post.json['blog_id'])
        path = '/api/v1/blog/1'
        response = self.client.get(path, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_editing_a_blog(self):
        post = self.client.post(path='/api/v1/blog', data=json.dumps(self.data), content_type='application/json')
        int_id = int(post.json['blog_id'])
        path = '/api/v1/blog/{}'.format(int_id)
        response = self.client.put(path, data=json.dumps(self.da), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_deleting_a_blog(self):
        post = self.client.post(path='/api/v1/blog', data=json.dumps(self.data), content_type='application/json')
        int_id = int(post.json['blog_id'])
        path = '/api/v1/blog/{}'.format(int_id)
        response = self.client.delete(path, content_type='application/json')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
