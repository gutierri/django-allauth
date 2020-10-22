import re
import urllib.request
from urllib.parse import (
    parse_qs,
    urlparse
)

import requests
from django.utils.http import urlencode
from allauth.socialaccount.providers.oauth2.client import (
    OAuth2Client,
    OAuth2Error
)


class MercadoLibreOAuth2Client(OAuth2Client):
    def get_redirect_url(self, authorization_url, extra_params):
        params = {
            "client_id": self.consumer_key,
            "redirect_uri": self.callback_url,
            "response_type": "code",
        }
        if self.state:
            params["state"] = self.state
        params.update(extra_params)
        url = "%s?%s" % (authorization_url, '&'.join([f'{k}={v}' for k, v in params.items()]))
        return url

    def get_access_token(self, code):
        data = {
            "redirect_uri": self.callback_url,
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.consumer_key,
            "client_secret": self.consumer_secret
        }
        params = None
        self._strip_empty_keys(data)
        url = self.access_token_url
        if self.access_token_method == "GET":
            params = data
            data = None
        # TODO: Proper exception handling
        resp = requests.request(
            self.access_token_method,
            url,
            params=params,
            data=data,
            headers={
                'accept': 'application/json',
                'content-type': 'application/x-www-form-urlencoded'
            },
        )
        access_token = None
        if resp.status_code in [200, 201]:
            # Weibo sends json via 'text/plain;charset=UTF-8'
            if (
                resp.headers["content-type"].split(";")[0] == "application/json"
                or resp.text[:2] == '{"'
            ):
                access_token = resp.json()
            else:
                access_token = dict(parse_qsl(resp.text))
        if not access_token or "access_token" not in access_token:
            raise OAuth2Error("Error retrieving access token: %s" % resp.content)
        return access_token
