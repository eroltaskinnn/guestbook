from app.models import  User, Entry
from django.db.models import Count, Max


class UserService:
    """
    A service class to handle user-related data retrieval.
    """

    def get_users_with_annotation(self):
        """
        Retrieves a list of users with annotations for total messages and last entry.

        Returns:
            QuerySet: A QuerySet of User objects with annotations for total messages and last entry.
        """
        # Annotate users with total messages and last entry, then order by name
        return User.objects.annotate(
            total_messages=Count('entries'),  # Count the total number of entries for each user
            last_entry=Max('entries__created_date')  # Get the created date of the last entry for each user
        ).order_by('name')  # Order the results by user name

    def get_last_entry_for_user(self, user):
        """
        Retrieves the last entry for a given user.

        Args:
            user (User): The user for which to retrieve the last entry.

        Returns:
            Entry: The last entry for the given user, or None if no entries exist.
        """
        # Filter entries by user and order by created date in descending order, then get the first result
        return Entry.objects.filter(user=user).order_by('-created_date').first()

    def get_users_data(self):
        """
        Retrieves a list of user data, including username and last entry information.

        Returns:
            list: A list of dictionaries containing user data.
        """
        # Get users with annotations
        users = self.get_users_with_annotation()
        # Initialize an empty list to store user data
        data = []
        # Iterate over each user
        for user in users:
            # Get the last entry for the user
            last_entry = self.get_last_entry_for_user(user)
            # Format the last entry string
            last_entry_str = f"{last_entry.subject}_{user.total_messages} | {last_entry.message}_{user.total_messages}" if last_entry else "No entries"
            # Append user data to the list
            data.append({
                "username": user.name,  # Store the username
                "last_entry": last_entry_str,  # Store the last entry string
            })
        # Return the list of user data
        return data