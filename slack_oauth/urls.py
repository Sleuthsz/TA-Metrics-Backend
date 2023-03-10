from django.urls import path

from slack_oauth.views import oauth_start, oauth_callback, id_token

urlpatterns = [
    path('slack/install', oauth_start, name='oauth_start'),
    path('slack/oauth_redirect', oauth_callback, name='oauth_callback'),
    path(r'slack/users/', id_token, name='id_token')
]
