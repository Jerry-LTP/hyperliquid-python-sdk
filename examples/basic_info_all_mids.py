from hyperliquid.info import Info
from hyperliquid.utils.types import L2BookData, Meta, SpotMeta
import os
from dotenv import load_dotenv
from hyperliquid.utils import constants

def main():
    load_dotenv()

    base_url = constants.MAINNET_LTP_API_URL
    if os.getenv("TEST") == "true":
        base_url = constants.TESTNET_LTP_API_URL

    info = Info(
        LT_API_KEY=os.getenv("LTP_API_KEY"),
        LT_API_SECRET=os.getenv("LTP_API_SECRET"),
        base_url=base_url,
        skip_ws=True
    )

    response = info.all_mids()
    print(response)

if __name__ == "__main__":
    main()