from django.test import TestCase
from ..models import Entry, User
from ..helpers.entry_service_helper import EntryService


class EntryServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(name='John Doe')
        self.entry1 = Entry.objects.create(user=self.user, subject='Test Subject 1', message='Test Message 1')
        self.entry2 = Entry.objects.create(user=self.user, subject='Test Subject 2', message='Test Message 2')
        self.entry_service = EntryService()

    def test_get_entries(self):
        entries = self.entry_service.get_entries()
        self.assertEqual(len(entries), 2)
        self.assertIn(self.entry1, entries)
        self.assertIn(self.entry2, entries)


    def test_serialize_entries(self):
        entries = self.entry_service.get_entries()
        serialized_entries = self.entry_service.serialize_entries(entries)
        self.assertEqual(len(serialized_entries), 2)
        self.assertEqual(serialized_entries[1]['subject'], 'Test Subject 1')
        self.assertEqual(serialized_entries[0]['subject'], 'Test Subject 2')
