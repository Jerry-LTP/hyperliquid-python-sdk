import json
import time
import example_utils

from hyperliquid.utils import constants

PURR = "PURR/USDC"
OTHER_COIN = "@8"
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

    address, info, exchange = example_utils.setup(ltp_api_key, ltp_api_secret, base_url, skip_ws=True)

    # Get the user state and print out position information
    spot_user_state = info.spot_user_state(address)
    if len(spot_user_state["balances"]) > 0:
        print("spot balances:")
        for balance in spot_user_state["balances"]:
            print(json.dumps(balance, indent=2))
    else:
        print("no available token balances")

    # Place an order that should rest by setting the price very low
    start_time = time.time()
    order_result = exchange.order(PURR, True, 80, 0.17, {"limit": {"tif": "Gtc"}})
    end_time = time.time()
    print("order time: ", end_time - start_time)
    print("order result: ", order_result)

    open_orders = info.open_orders(address)
    print("open orders: ", open_orders)


    # Query the order status by oid
    if order_result["status"] == "ok":
        status = order_result["response"]["data"]["statuses"][0]
        if "resting" in status:
            start_time = time.time()
            order_status = info.query_order_by_oid(address, status["resting"]["oid"])
            end_time = time.time()
            print("query order by oid time: ", end_time - start_time)
            print("Order status by oid:", order_status)

    # Cancel the order
    if order_result["status"] == "ok":
        status = order_result["response"]["data"]["statuses"][0]
        if "resting" in status:
            start_time = time.time()
            cancel_result = exchange.cancel(PURR, status["resting"]["oid"])
            end_time = time.time()
            print("cancel time: ", end_time - start_time)
            print("cancel result: ", cancel_result)
    
    start_time = time.time()
    open_orders = info.open_orders(address)
    end_time = time.time()
    print("open orders time: ", end_time - start_time)
    print("open orders: ", open_orders)


if __name__ == "__main__":
    main()
