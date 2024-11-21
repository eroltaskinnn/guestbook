import unittest
from django.test import TestCase
from django.db.models import Count, Max
from app.helpers.user_service_helper import UserService
from app.models import User, Entry

class UserServiceTestCase(TestCase):

    def setUp(self):
        self.user_service = UserService()
        self.user1 = User.objects.create(name='John Doe')
        self.user2 = User.objects.create(name='Jane Doe')
        Entry.objects.create(user=self.user1, subject='Test Subject 1', message='Test Message 1')
        Entry.objects.create(user=self.user1, subject='Test Subject 2', message='Test Message 2')
        Entry.objects.create(user=self.user2, subject='Test Subject 3', message='Test Message 3')

    def test_get_users_with_annotation(self):
        users = self.user_service.get_users_with_annotation()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].name, 'Jane Doe')
        self.assertEqual(users[0].total_messages, 1)
        self.assertIsNotNone(users[0].last_entry)
        self.assertEqual(users[1].name, 'John Doe')
        self.assertEqual(users[1].total_messages, 2)
        self.assertIsNotNone(users[1].last_entry)

    def test_get_last_entry_for_user(self):
        """
        Tests the get_last_entry_for_user method.

        Returns:
            None
        """
        # Create a test user
        user = User.objects.create(name='John Smith')

        # Create a test entry for the user
        entry = Entry.objects.create(user=user, subject='Test Subject', message='Test Message')

        # Get the last entry for the user
        last_entry = self.user_service.get_last_entry_for_user(user)

        # Assert that the last entry is the one we created
        self.assertEqual(last_entry, entry)

        # Create another entry for the user
        another_entry = Entry.objects.create(user=user, subject='Another Test Subject', message='Another Test Message')

        # Get the last entry for the user again
        last_entry_again = self.user_service.get_last_entry_for_user(user)

        # Assert that the last entry is now the new one we created
        self.assertEqual(last_entry_again, another_entry)

        # Delete all entries for the user
        Entry.objects.filter(user=user).delete()

        # Get the last entry for the user again
        last_entry_none = self.user_service.get_last_entry_for_user(user)

        # Assert that the last entry is now None
        self.assertIsNone(last_entry_none)