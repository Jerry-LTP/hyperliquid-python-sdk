import example_utils

from hyperliquid.utils import constants
from hyperliquid.utils.types import Cloid
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

    cloid = Cloid.from_str("0x00000000000000000000000000000001")
    # Users can also generate a cloid from an int
    # cloid = Cloid.from_int(1)
    # Place an order that should rest by setting the price very low
    order_result = exchange.order("BTC", True, 0.01, 41100, {"limit": {"tif": "Gtc"}}, cloid=cloid)
    print(order_result)

    # Query the order status by cloid
    order_status = info.query_order_by_cloid(address, cloid)
    print("Order status by cloid:", order_status)

    # Non-existent cloid example
    invalid_cloid = Cloid.from_int(2)
    order_status = info.query_order_by_cloid(address, invalid_cloid)
    print("Order status by cloid:", order_status)

    # Cancel the order by cloid
    if order_result["status"] == "ok":
        status = order_result["response"]["data"]["statuses"][0]
        if "resting" in status:
            cancel_result = exchange.cancel_by_cloid("BTC", cloid)
            print(cancel_result)


if __name__ == "__main__":
    main()
