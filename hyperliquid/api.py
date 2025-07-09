import json
import logging
import time
import hmac
import hashlib
from json import JSONDecodeError

import requests

from hyperliquid.utils.constants import MAINNET_API_URL
from hyperliquid.utils.error import ClientError, ServerError
from hyperliquid.utils.types import Any


class API:
    def __init__(self, LT_API_KEY, LT_API_SECRET, base_url=None):
        self.base_url = base_url or MAINNET_API_URL
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._logger = logging.getLogger(__name__)
        self.ltp_api_key = LT_API_KEY
        self.ltp_api_secret = LT_API_SECRET

    def post(self, url_path: str, payload: Any = None) -> Any:
        # Build request body
        if payload:
            new_body = {"body": json.dumps(payload)}
        else:
            new_body = {}

        # Build encryption string
        to_encrypt = ""
        if new_body:
            for key, value in new_body.items():
                to_encrypt += f"{key}={value}&"
        
        # Add timestamp
        now = int(time.time())
        to_encrypt += str(now)

        # Create HMAC signature
        hmac_obj = hmac.new(
            self.ltp_api_secret.encode('utf-8'),
            to_encrypt.encode('utf-8'),
            hashlib.sha256
        )
        signature = hmac_obj.hexdigest()

        # Set request headers
        headers = {
            "Content-Type": "application/json",
            "X-MBX-APIKEY": self.ltp_api_key,
            "signature": signature,
            "nonce": str(now)
        }

        url = self.base_url + url_path
        response = self.session.post(url, json=new_body, headers=headers)
        self._handle_exception(response)
        try:
            return response.json()
        except ValueError:
            return {"error": f"Could not parse JSON: {response.text}"}

    def _handle_exception(self, response):
        status_code = response.status_code
        if status_code < 400:
            return
        if 400 <= status_code < 500:
            try:
                err = json.loads(response.text)
            except JSONDecodeError:
                raise ClientError(status_code, None, response.text, None, response.headers)
            if err is None:
                raise ClientError(status_code, None, response.text, None, response.headers)
            error_data = err.get("data")
            raise ClientError(status_code, err["error"], response.headers, error_data)
        raise ServerError(status_code, response.text)
