# LTP Hyperliquid SDK wrapper

this is a wrapper of Hyperliquid Python SDK https://github.com/hyperliquid-dex/hyperliquid-python-sdk

## Installation
```bash
pip install git+https://github.com/Jerry-LTP/hyperliquid-python-sdk.git
```
## Extra Configuration 

you should add LTP API key pair to Info and Exchange struct. (see [example](https://github.com/Jerry-LTP/hyperliquid-python-sdk/blob/master/examples/example_utils.py#L11))

- only Info and Exchange struct is updated to support LTP authentication, no change for ws.
- in order to not break the python SDK code, you still need to provide a Hyperliquid api key although we dont need it any more. you may just provide a random generated ethereum private key, or follow the offcial processure https://app.hyperliquid.xyz/API. (see [example](https://github.com/Jerry-LTP/hyperliquid-python-sdk/blob/master/examples/example_utils.py#L11), the *secret_key* in *config.json*)
- you need to specify the subaccount in request, LTP server will validate that subaccount is attaced to your LTP account. (If you dont have one, please contact LTP service)

## Usage Examples

See [examples](examples) for more complete examples. You can also checkout the repo and run any of the examples after configuring your private key e.g. 

## CAUTIONS

LTP only update some of the the info and exchange http interface, for ws part, it stays the same as official SDK.

you may check this diff 
https://github.com/hyperliquid-dex/hyperliquid-python-sdk/compare/master...Jerry-LTP:hyperliquid-python-sdk:master

to see the change of ltp on the original repo