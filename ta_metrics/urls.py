from django.urls import path
from .views import get_tickets_and_wait

urlpatterns = [
    path('ticket_wait', get_tickets_and_wait, name='get_tickets_and_wait')
]
