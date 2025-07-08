import json

import example_utils

from hyperliquid.utils import constants
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    ltp_api_key = os.getenv("LTP_API_KEY")
    ltp_api_secret = os.getenv("LTP_API_SECRET")
    
    address, info, exchange = example_utils.setup(ltp_api_key, ltp_api_secret, constants.TESTNET_LTP_API_URL, skip_ws=True)
    print("address", address)

    # Get the user state and print out leverage information for ETH
    user_state = info.user_state(address)
    print("user_state", user_state)
    for asset_position in user_state["assetPositions"]:
        if asset_position["position"]["coin"] == "ETH":
            print("Current leverage for ETH:", json.dumps(asset_position["position"]["leverage"], indent=2))

    # Set the ETH leverage to 21x (cross margin)
    print("btc", exchange.update_leverage(21, "BTC"))

    # Set the ETH leverage to 22x (isolated margin)
    print("eth", exchange.update_leverage(21, "ETH", False))

    # Add 1 dollar of extra margin to the ETH position
    #print("eth isolated margin", exchange.update_isolated_margin(1, "ETH"))

    # Get the user state and print out the final leverage information after our changes
    user_state = info.user_state(address)
    for asset_position in user_state["assetPositions"]:
        if asset_position["position"]["coin"] == "ETH":
            print("Current leverage for ETH:", json.dumps(asset_position["position"]["leverage"], indent=2))


if __name__ == "__main__":
    main()
