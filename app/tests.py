# guestbook_app/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Entry

class GuestBookTest(APITestCase):
    def test_create_entry(self):
        url = reverse('create-entry')
        data = {'name': 'John Doe', 'subject': 'Test Subject', 'message': 'Test Message'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entry.objects.count(), 1)

    def test_get_entries(self):
        url = reverse('get-entries')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users(self):
        url = reverse('get-users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)