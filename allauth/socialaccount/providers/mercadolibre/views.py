import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import MercadoLibreProvider
from .client import MercadoLibreOAuth2Client


class MercadoLibreOAuth2Adapter(OAuth2Adapter):
    provider_id = MercadoLibreProvider.id
    client_class = MercadoLibreOAuth2Client
    access_token_url = "https://api.mercadolibre.com/oauth/token"
    authorize_url = "http://auth.mercadolivre.com.br/authorization"
    profile_url = "https://api.mercadolibre.com/users/me"

    def complete_login(self, request, app, token, **kwargs):
        extra_data = requests.get(
            self.profile_url, params={"access_token": token.token}
        )

        return self.get_provider().sociallogin_from_response(request, extra_data.json())


oauth2_login = OAuth2LoginView.adapter_view(MercadoLibreOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(MercadoLibreOAuth2Adapter)
