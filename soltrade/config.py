import os
import json
import base58

from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solana.rpc.api import Client
from soltrade.log import log_general
from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()

        self.api_key = None
        self.private_key = None
        self.custom_rpc_https = None
        self.primary_mint = None
        self.primary_mint_symbol = None
        self.sol_mint = "So11111111111111111111111111111111111111112"
        self.secondary_mint = None
        self.secondary_mint_symbol = None
        self.price_update_seconds = None
        self.trading_interval_minutes = None
        self.slippage = None  # BPS
        self.computeUnitPriceMicroLamports = None
        self.stoploss = None
        self.trailing_stoploss = None
        self.trailing_stoploss_target = None
        self.telegram = None
        self.tg_bot_token = None
        self.tg_bot_uid = None
        self.load_config()

    def load_config(self):
        self.api_key = os.getenv('API_KEY')
        self.private_key = os.getenv("WALLET_PRIVATE_KEY")
        self.custom_rpc_https = os.getenv("custom_rpc_https", "https://api.mainnet-beta.solana.com/")
        self.primary_mint = os.getenv("PRIMARY_MINT", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
        self.primary_mint_symbol = os.getenv("PRIMARY_MINT_SYMBOL", "USD")
        self.secondary_mint = os.getenv("SECONDARY_MINT", "")
        self.secondary_mint_symbol = os.getenv("SECONDARY_MINT_SYMBOL", "UNKNOWN")
        self.price_update_seconds = int(os.getenv("PRICE_UPDATE_SECONDS") or 60)
        self.trading_interval_minutes = int(os.getenv("TRADING_INTERVALS_MINUTE") or 1)
        self.slippage = int(os.getenv("SLIPPAGE") or 50)

        # DEFAULT FEE OF ROUGHLY $0.04 TODAY
        self.computeUnitPriceMicroLamports = int(os.getenv("COMPUTE_UNIT_PRICE_MICRO_LAMPORTS") or 20 * 14000)

        ### THESE VALUES DETERMINE STRATEGY, STOPLOSS, AND TELEGRAM.
        ### THEY WILL BE USED AFTER CONFLICTS ARE RESOLVED AND CODE IS BETTER UNDERSTOOD.
        ### I AM DOING THIS ON A FLIGHT SO IGNORE THE ISSUES PLEASE.
        
        #self.strategy = config_data.get("strategy", "default")
        #self.stoploss = config_data["stoploss"]
        #self.trailing_stoploss = config_data["trailing_stoploss"]
        #self.trailing_stoploss_target = config_data["trailing_stoploss_target"]
        #self.telegram = config_data.get("telegram", False)
        #if self.telegram == True:
        #    self.tg_bot_token = config_data["tg_bot_token"]
        #    self.tg_bot_uid = config_data["tg_bot_uid"]

    @property
    def keypair(self) -> Keypair:
        try:
            b58_string = self.private_key
            keypair = Keypair.from_base58_string(b58_string)
            # print(f"Using Wallet: {keypair.pubkey()}")

            return keypair
        except Exception as e:
            log_general.error(f"Error decoding private key: {e}")
            exit(1)

    @property
    def public_address(self) -> Pubkey:
        return self.keypair.pubkey()

    @property
    def client(self) -> Client:
        rpc_url = self.custom_rpc_https
        return Client(rpc_url)

    @property
    def decimals(self) -> int:
        response = self.client.get_account_info_json_parsed(Pubkey.from_string(config().secondary_mint)).to_json()
        json_response = json.loads(response)
        value = 10 ** json_response["result"]["value"]["data"]["parsed"]["info"]["decimals"]
        return value


_config_instance = None


def config() -> Config:
    global _config_instance
    _config_instance = Config()
    return _config_instance
