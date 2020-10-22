from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import MercadoLibreProvider


urlpatterns = default_urlpatterns(MercadoLibreProvider)
