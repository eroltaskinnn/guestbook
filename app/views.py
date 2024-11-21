from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .helpers.entry_service_helper import EntryService
from .helpers.user_service_helper import UserService
from .models import User, Entry
from .serializers import UserSerializer, EntrySerializer
from django.core.paginator import Paginator
from django.db.models import Count, Max


class CreateEntryView(APIView):
    def post(self, request):
        name = request.data.get('name')
        subject = request.data.get('subject')
        message = request.data.get('message')

        user, created = User.objects.get_or_create(name=name)
        entry = Entry.objects.create(user=user, subject=subject, message=message)

        return Response(EntrySerializer(entry).data, status=status.HTTP_201_CREATED)

class GetEntriesView(APIView):
    def __init__(self):
        self.entry_service = EntryService()

    def get(self, request):
        entries = self.entry_service.get_entries()
        page = self.entry_service.paginate_entries(entries, request)
        serialized_entries = self.entry_service.serialize_entries(page.object_list)
        response_data = self.entry_service.format_response(page, serialized_entries)

        return Response(response_data)

class GetUsersDataView(APIView):
    def __init__(self):
        self.user_data_service = UserService()

    def get(self, request):
        data = self.user_data_service.get_users_data()
        return Response({"users": data})