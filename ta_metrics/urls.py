from django.urls import path
from . import views

urlpatterns = [
    path('/ticket_wait', get_tickets_and_wait.view_function, name='get_tickets_and_wait')
]
