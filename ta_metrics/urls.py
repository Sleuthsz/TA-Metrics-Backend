from django.urls import path
from .views import get_tickets_and_wait, get_summary_stats

urlpatterns = [
    path('ticket_wait', get_tickets_and_wait, name='get_tickets_and_wait'),
    path('summary_stats', get_summary_stats, name='get_summary_stats'),
]
