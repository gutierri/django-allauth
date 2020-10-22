from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class MercadoLibreProvider(OAuth2Provider):
    id = 'mercadolibre'
    name = 'Mercado Libre'

    def extract_uid(self, data):
        return data['id']


provider_classes = [MercadoLibreProvider]
