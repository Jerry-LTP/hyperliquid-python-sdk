from hyperliquid.info import Info
from hyperliquid.utils.types import L2BookData, Meta, SpotMeta
import os
from dotenv import load_dotenv
from hyperliquid.utils import constants
import example_utils

def main():
    load_dotenv()
    ltp_api_key = os.getenv("LTP_API_KEY")
    ltp_api_secret = os.getenv("LTP_API_SECRET")
    address, info, exchange = example_utils.setup(ltp_api_key, ltp_api_secret, constants.MAINNET_LTP_API_URL, skip_ws=True)

    base_url = constants.MAINNET_LTP_API_URL
    if os.getenv("TEST") == "true":
        base_url = constants.TESTNET_LTP_API_URL

    print(base_url)
    info = Info(
        LT_API_KEY=ltp_api_key,
        LT_API_SECRET=ltp_api_secret,
        base_url=base_url,
        skip_ws=True
    )

    response = info.user_state(address)
    print(response)

if __name__ == "__main__":
    main()