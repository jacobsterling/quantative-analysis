from dotenv import load_dotenv
from os import getenv

load_dotenv()

KUCOIN_CONFIG = {
    "trading_mode": "spot",
    "exchange": {
        "name": "kucoin",
        "ccxt_config": {},
        "ccxt_async_config": {},
        "skip_pair_validation": True,
        "pair_whitelist": [".*/USDT:USDT", ".*/USDT"],
        "pair_blacklist": ["KCS/USDT"],
        "key": getenv("KUCOIN_API"),
        "secret": getenv("KUCOIN_SECRET"),
    },
    "pairs": ["ETH/USDT"],
    "pairlists": [{"method": "StaticPairList", "allow_inactive": True}],
}
