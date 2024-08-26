from dataclasses import dataclass


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
