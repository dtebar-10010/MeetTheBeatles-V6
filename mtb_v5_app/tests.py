from django.test import TestCase
from django.urls import reverse


class HealthTest(TestCase):
    def test_health_endpoint(self):
        url = reverse('health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})
