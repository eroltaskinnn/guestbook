from django.urls import path
from .views import CreateEntryView, GetEntriesView, GetUsersDataView

urlpatterns = [
    path('create_entry/', CreateEntryView.as_view(), name='create_entry'),
    path('get_entries/', GetEntriesView.as_view(), name='get_entries'),
    path('get_users_data/', GetUsersDataView.as_view(), name='get_users_data'),
]