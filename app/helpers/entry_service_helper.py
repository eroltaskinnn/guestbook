from app.models import  Entry
from app.serializers import  EntrySerializer

from django.core.paginator import Paginator

class EntryService:
    """
    A service class to handle entry-related data retrieval and pagination.
    """

    def get_entries(self):
        """
        Retrieves all entries from the database.

        Returns:
            QuerySet: A QuerySet of all Entry objects.
        """
        # Retrieve all entries from the database
        return Entry.objects.all()

    def paginate_entries(self, entries, request):
        """
        Paginates the given entries based on the request.

        Args:
            entries (QuerySet): A QuerySet of Entry objects to paginate.
            request (Request): The HTTP request object.

        Returns:
            Page: A Page object containing the paginated entries.
        """
        # Create a paginator with 3 entries per page
        paginator = Paginator(entries, 3)
        # Get the page number from the request, defaulting to 1
        page_number = request.GET.get('page', 1)
        # Return the paginated page
        return paginator.get_page(page_number)

    def serialize_entries(self, entries):
        """
        Serializes the given entries using the EntrySerializer.

        Args:
            entries (QuerySet): A QuerySet of Entry objects to serialize.

        Returns:
            list: A list of serialized entry data.
        """
        # Serialize the entries using the EntrySerializer
        return EntrySerializer(entries, many=True).data

    def format_response(self, page, serialized_entries):
        """
        Formats the response data for the paginated entries.

        Args:
            page (Page): A Page object containing the paginated entries.
            serialized_entries (list): A list of serialized entry data.

        Returns:
            dict: A dictionary containing the response data.
        """
        # Create a dictionary to store the response data
        return {
            # The total count of entries
            'count': page.paginator.count,
            # The number of entries per page
            'page_size': page.paginator.per_page,
            # The total number of pages
            'total_pages': page.paginator.num_pages,
            # The current page number
            'current_page': page.number,
            # Links to the next and previous pages
            'links': {
                # The next page number, or None if there is no next page
                'next': page.next_page_number() if page.has_next() else None,
                # The previous page number, or None if there is no previous page
                'previous': page.previous_page_number() if page.has_previous() else None
            },
            # The serialized entry data
            'entries': serialized_entries
        }