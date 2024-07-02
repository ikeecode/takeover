# chat/urls.py
from django.urls import path
from .views import send_message, takeover, get_messages, handover_to_ai

urlpatterns = [
    path('send_message/', send_message, name='send_message'),
    path('takeover/', takeover, name='takeover'),
    path('messages/<str:user>/', get_messages, name='get_messages'),
    path('handover_to_ai/', handover_to_ai, name='handover_to_ai'),
]
