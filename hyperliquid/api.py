import json
import logging
import time
import hmac
import hashlib
from json import JSONDecodeError

import requests

from hyperliquid.utils.constants import MAINNET_API_URL
from hyperliquid.utils.error import ClientError, ServerError
from hyperliquid.utils.types import Any, Optional


class API:
    def __init__(
        self,
        LT_API_KEY: Optional[str] = None,
        LT_API_SECRET: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        self.base_url = base_url or MAINNET_API_URL
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._logger = logging.getLogger(__name__)
        self.ltp_api_key = LT_API_KEY
        self.ltp_api_secret = LT_API_SECRET
        self.timeout = timeout

    def post(self, url_path: str, payload: Any = None) -> Any:
        payload = payload or {}
        url = self.base_url + url_path

        if self.ltp_api_key and self.ltp_api_secret:
            if payload:
                new_body = {"body": json.dumps(payload)}
            else:
                new_body = {}
            to_encrypt = ""
            if new_body:
                for key, value in new_body.items():
                    to_encrypt += f"{key}={value}&"
            now = int(time.time())
            to_encrypt += str(now)
            hmac_obj = hmac.new(
                self.ltp_api_secret.encode("utf-8"),
                to_encrypt.encode("utf-8"),
                hashlib.sha256,
            )
            signature = hmac_obj.hexdigest()
            headers = {
                "Content-Type": "application/json",
                "X-MBX-APIKEY": self.ltp_api_key,
                "signature": signature,
                "nonce": str(now),
            }
            response = self.session.post(url, json=new_body, headers=headers, timeout=self.timeout)
        else:
            response = self.session.post(url, json=payload, timeout=self.timeout)

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
            raise ClientError(status_code, err["code"], err["msg"], response.headers, error_data)
        raise ServerError(status_code, response.text)
