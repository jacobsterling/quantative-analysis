from dotenv import load_dotenv
from os import getenv
from dataclasses import dataclass

load_dotenv()


@dataclass(frozen=True)
class Trade:
    symbol: str
    price: float
    quantity: int


@dataclass(frozen=True)
class CCTXExchangeConfig:
    name: str
    key: str
    secret: str
    password: str | None = None
    pair_whitelist: list[str]
    pair_blacklist: list[str]
    ccxt_config: dict = {}
    ccxt_async_config: dict = {}
    skip_pair_validation: bool = True


@dataclass(frozen=True)
class CCTXConfig:
    trading_mode: str
    exchange: CCTXExchangeConfig
    pairs: list


KUCOIN_CONFIG: CCTXExchangeConfig = CCTXExchangeConfig(
    name="kucoin",
    pair_whitelist=[".*/USDT:USDT", ".*/USDT"],
    pair_blacklist=["KCS/USDT"],
    key=getenv("KUCOIN_API"),
    secret=getenv("KUCOIN_SECRET"),
    password=getenv("KUCOIN_PASSWORD"),
)
