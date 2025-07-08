import example_utils

from hyperliquid.utils import constants
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    ltp_api_key = os.getenv("LTP_API_KEY")
    ltp_api_secret = os.getenv("LTP_API_SECRET")   
    address, info, exchange = example_utils.setup(ltp_api_key, ltp_api_secret, constants.TESTNET_LTP_API_URL, skip_ws=True)

    open_orders = info.open_orders(address)
    for open_order in open_orders:
        print(f"cancelling order {open_order}")
        exchange.cancel(open_order["coin"], open_order["oid"])


if __name__ == "__main__":
    main()
