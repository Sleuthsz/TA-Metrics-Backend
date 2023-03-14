from django.urls import path
from .views import daily_tickets_waits, get_summary_stats

urlpatterns = [
    path('ticket_wait', daily_tickets_waits, name='daily_tickets_waits'),
    path('summary_stats', get_summary_stats, name='get_summary_stats'),
]
