import time

import example_utils

from hyperliquid.utils import constants
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    ltp_api_key = os.getenv("LTP_API_KEY")
    ltp_api_secret = os.getenv("LTP_API_SECRET")    
    address, info, exchange = example_utils.setup(ltp_api_key, ltp_api_secret, constants.TESTNET_LTP_API_URL, skip_ws=True)

    coin = "BTC"
    is_buy = True
    sz = 0.001

    print(f"We try to Market {'Buy' if is_buy else 'Sell'} {sz} {coin}.")

    order_result = exchange.market_open(coin, is_buy, sz, None, 0.01)
    if order_result["status"] == "ok":
        for status in order_result["response"]["data"]["statuses"]:
            try:
                filled = status["filled"]
                print(f'Order #{filled["oid"]} filled {filled["totalSz"]} @{filled["avgPx"]}')
            except KeyError:
                print(f'Error: {status["error"]}')

        print("We wait for 2s before closing")
        time.sleep(2)

        print(f"We try to Market Close all {coin}.")
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
