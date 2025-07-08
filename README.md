# LTP Hyperliquid SDK wrapper

this is a wrapper of Hyperliquid Python SDK https://github.com/hyperliquid-dex/hyperliquid-python-sdk

## Installation
```bash
pip install git+https://github.com/Jerry-LTP/hyperliquid-python-sdk.git
```
## Configuration 

almost the same as official SDK:

- Set the public key as the `account_address` in examples/config.json.
- Set your private key as the `secret_key` in examples/config.json.
- See the example of loading the config in examples/example_utils.py
### [Optional] Generate a new API key for an API Wallet
Generate and authorize a new API private key on https://app.hyperliquid.xyz/API, and set the API wallet's private key as the `secret_key` in examples/config.json. Note that you must still set the public key of the main wallet *not* the API wallet as the `account_address` in examples/config.json

**DIFFERENCE**

you need to get LTP API KEY/Secret, and ask LTP manager to setup hyperliquid subaccount for you.

**You need to specify subaccount address in each call, no default subaccount any more**



## Usage Examples

See [examples](examples) for more complete examples. You can also checkout the repo and run any of the examples after configuring your private key e.g. 

## CAUTIONS

LTP only update some of the the info and exchange http interface, for ws part, it stays the same as official SDK.