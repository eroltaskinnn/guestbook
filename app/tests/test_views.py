from django.test import TestCase, Client
from django.urls import reverse
from ..models import User, Entry
from rest_framework import status

from ..serializers import EntrySerializer


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(name='John Doe')
        self.entry1 = Entry.objects.create(user=self.user, subject='Test Subject 1', message='Test Message 1')
        self.entry2 = Entry.objects.create(user=self.user, subject='Test Subject 2', message='Test Message 2')

    def test_get_users_data_view(self):
        response = self.client.get(reverse('get_users_data'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['users']), 1)
        self.assertEqual(response.json()['users'][0]['username'], 'John Doe')

    def test_get_entries_view(self):
        response = self.client.get(reverse('get_entries'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['entries']), 2)
        self.assertEqual(response.json()['entries'][1]['subject'], 'Test Subject 1')
        self.assertEqual(response.json()['entries'][0]['subject'], 'Test Subject 2')

    def test_get_entries_view_empty_page(self):
        response = self.client.get(reverse('get_entries'), {'page': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['entries']), 2)

    def test_create_entry(self):
        url = reverse('create_entry')
        data = {
            'name': 'John Doe',
            'subject': 'Test Subject',
            'message': 'Test Message'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entry.objects.count(), 3)

        entry = Entry.objects.first()
        self.assertEqual(entry.user.name, data['name'])
        self.assertEqual(entry.subject, data['subject'])
        self.assertEqual(entry.message, data['message'])

        # Verify response data
        serializer = EntrySerializer(entry)
        self.assertEqual(response.data, serializer.data)