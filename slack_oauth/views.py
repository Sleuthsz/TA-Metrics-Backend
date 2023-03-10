import logging

import jwt
import redis
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from slack_sdk import WebClient
from slack_sdk.oauth import OpenIDConnectAuthorizeUrlGenerator, RedirectUriPageRenderer
from slack_sdk.oauth.state_store import FileOAuthStateStore

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

client_id = settings.SLACK_CLIENT_ID
client_secret = settings.SLACK_CLIENT_SECRET
redirect_uri = settings.SLACK_REDIRECT_URL
scopes = ['openid', 'email', 'profile']

state_store = FileOAuthStateStore(expiration_seconds=300)

authorization_url_generator = OpenIDConnectAuthorizeUrlGenerator(
    client_id=client_id,
    scopes=scopes,
    redirect_uri=redirect_uri
)

redirect_page_renderer = RedirectUriPageRenderer(
    install_path='/slack/install',
    redirect_uri_path='/slack/oauth_redirect'
)

redis_client = redis.Redis(host='localhost', port=6379, db=0)


@api_view(['GET'])
def oauth_start(request):
    state = state_store.issue()
    url = authorization_url_generator.generate(state=state)
    return JsonResponse({'redirect_url': url})


@api_view(['GET'])
def oauth_callback(request):
    code = request.GET.get('code')
    if code is not None:
        state = request.GET.get('state')
        if state_store.consume(state):
            try:
                token_response = WebClient().openid_connect_token(
                    client_id=client_id,
                    client_secret=client_secret,
                    code=code
                )
                logger.info(f"openid.connect.token response: {token_response}\n")
                token = token_response.get("id_token")
                claims = jwt.decode(token, options={"verify_signature": False}, algorithms=["RS256"])
                logger.info(f"claims (decoded id_token): {claims}\n")

                user_token = token_response.get("access_token")
                user_info_response = WebClient(token=user_token).openid_connect_userInfo()
                logger.info(f"\nopenid.connect.userInfo response: {user_info_response}\n")
                user_id = user_info_response.get("https://slack.com/user_id")

                redis_client.set(f'{user_id}', token)
                return redirect(f'http://localhost:3000/login/?id_token={token}')
            except Exception as e:
                logger.exception('Failed to perform openid.connect.token API call\n')
                logger.error(f'{e}\n')
                return redirect_page_renderer.render_failure_page('Failed to perform openid.connect.token API call')
        else:
            return redirect_page_renderer.render_failure_page('The state value is already expired')
    else:
        error = request.GET.get('error')
        return HttpResponseBadRequest(f'Something is wrong with the installation (error: {error})')


@api_view(['GET'])
def id_token(request):
    user_id = request.GET.get('user_id')
    logger.info(f'USER ID: {user_id}')
    retrieved_id_token = redis_client.get(user_id)
    logger.info(f'ID TOKEN: {retrieved_id_token}')
    return JsonResponse({
        'id_token': retrieved_id_token.decode('utf-8')
    })
