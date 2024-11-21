# app/serializers.py
from rest_framework import serializers
from .models import Entry, User

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['user', 'subject', 'message']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'created_date']
