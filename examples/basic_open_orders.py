import json

import example_utils

from hyperliquid.utils import constants

PURR = "PURR/USDC"
OTHER_COIN = "@197"
OTHER_COIN_NAME = "KORILA/USDC"
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    ltp_api_key = os.getenv("LTP_API_KEY")
    ltp_api_secret = os.getenv("LTP_API_SECRET")
    base_url = constants.MAINNET_LTP_API_URL

    if os.getenv("TEST") == "true":
        base_url = constants.TESTNET_LTP_API_URL

    address, info, exchange = example_utils.setup(ltp_api_key, ltp_api_secret, base_url=base_url, skip_ws=True)

    # Get the user state and print out position information
    spot_user_state = info.spot_user_state(address)
    if len(spot_user_state["balances"]) > 0:
        print("spot balances:")
        for balance in spot_user_state["balances"]:
            print(json.dumps(balance, indent=2))
    else:
        print("no available token balances")

    open_orders = info.open_orders(address)
    if len(open_orders) > 0:
        print(open_orders)
    else:
        print("no open orders")


if __name__ == "__main__":
    main()
