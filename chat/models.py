# # chat/models.py
# from django.db import models

# class Message(models.Model):
#     sender = models.CharField(max_length=255)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

# class ChatSession(models.Model):
#     user = models.CharField(max_length=255)
#     is_human = models.BooleanField(default=False)
#     last_active = models.DateTimeField(auto_now=True)


# chat/models.py
from django.db import models

class Message(models.Model):
    sender = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey('ChatSession', on_delete=models.CASCADE, related_name='messages')

class ChatSession(models.Model):
    user = models.CharField(max_length=255)  # This represents the customer
    is_human = models.BooleanField(default=False)
    last_active = models.DateTimeField(auto_now=True)
    business_owner = models.CharField(max_length=255, blank=True, null=True)  # To track the business owner handling the session
