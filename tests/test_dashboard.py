import unittest
import json
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app import app

class DashboardTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_metrics_endpoint(self):
        response = self.app.get('/metrics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('techné', data)
        self.assertIn('iae', data)
        self.assertIn('harmony', data)
        self.assertIn('ethos', data)

    def test_narrative_endpoint(self):
        response = self.app.get('/narrative')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('text', data)

    def test_veto_endpoint(self):
        response = self.app.post('/veto')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')

if __name__ == '__main__':
    unittest.main()
