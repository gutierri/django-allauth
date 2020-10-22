from django.test.utils import override_settings

from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase

from .provider import MercadoLibreProvider


@override_settings(SOCIALACCOUNT_QUERY_EMAIL=True)
class MercadoLibreOAuth2Tests(OAuth2TestsMixin, TestCase):
    provider_id = MercadoLibreProvider.id
