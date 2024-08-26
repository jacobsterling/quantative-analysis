from dotenv import load_dotenv
from os import getenv
from .fixtures import CCTXExchangeConfig

load_dotenv()

KUCOIN_CONFIG: CCTXExchangeConfig = CCTXExchangeConfig(
    name="kucoin",
    pair_whitelist=[".*/USDT:USDT", ".*/USDT"],
    pair_blacklist=["KCS/USDT"],
    key=getenv("KUCOIN_API"),
    secret=getenv("KUCOIN_SECRET"),
)
