import example_utils

from hyperliquid.utils import constants
from hyperliquid.utils.types import Cloid
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    ltp_api_key = os.getenv("LTP_API_KEY")
    ltp_api_secret = os.getenv("LTP_API_SECRET")   
    address, info, exchange = example_utils.setup(ltp_api_key, ltp_api_secret, constants.TESTNET_LTP_API_URL, skip_ws=True)

    cloid = Cloid.from_str("0x00000000000000000000000000000001")
    # Place an order that should rest by setting the price very low
    order_result = exchange.order("BTC", True, 0.01, 40000, {"limit": {"tif": "Gtc"}}, cloid=cloid)
    print(order_result)

    # Modify the order by oid
    if order_result["status"] == "ok":
        status = order_result["response"]["data"]["statuses"][0]
        if "resting" in status:
            oid = status["resting"]["oid"]
            order_status = info.query_order_by_oid(address, oid)
            print("Order status by oid:", order_status)

            modify_result = exchange.modify_order(oid, "BTC", True, 0.01, 41000, {"limit": {"tif": "Gtc"}}, cloid=cloid)
            print("modify result with oid:", modify_result)

            modify_result = exchange.modify_order(cloid, "BTC", True, 0.01, 42000, {"limit": {"tif": "Gtc"}})
            print("modify result with cloid:", modify_result)


if __name__ == "__main__":
    main()
