import os

import pytest


@pytest.fixture
def ltp_creds():
    key = os.environ.get("LTP_API_KEY")
    secret = os.environ.get("LTP_API_SECRET")
    if not key or not secret:
        pytest.skip("Set LTP_API_KEY and LTP_API_SECRET to run these tests")
    return key, secret
