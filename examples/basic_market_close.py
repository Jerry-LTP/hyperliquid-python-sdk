import time

import example_utils

from hyperliquid.utils import constants
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

    coin = "BTC"
    is_buy = True
    sz = 0.001

    print(f"We try to Market {'Buy' if is_buy else 'Sell'} {sz} {coin}.")

    order_result = exchange.market_close(coin)
    if order_result["status"] == "ok":
        for status in order_result["response"]["data"]["statuses"]:
            try:
                filled = status["filled"]
                print(f'Order #{filled["oid"]} filled {filled["totalSz"]} @{filled["avgPx"]}')
            except KeyError:
                print(f'Error: {status["error"]}')
        


if __name__ == "__main__":
    main()
