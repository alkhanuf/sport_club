from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient
from sportsclub.models import *

# Create your tests here.
class ClientsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        r = self.client.get('/api/Client/')
        print(r)