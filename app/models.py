# guestbook_app/models.py

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique name
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']  # Default ordering

    def __str__(self):
        return f"{self.user.name} - {self.subject}"