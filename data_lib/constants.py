from dataclasses import dataclass
from pandas import Timestamp


@dataclass(frozen=True)
class Trade:
    symbol: str
    price: float
    quantity: float
    side: str

    stop_loss_price: float  # price to trigger stop-loss orders
    stop: str  # 'up' or 'down', the direction the stopPrice is triggered from, requires stopPrice. down: Triggers when the price reaches or goes below the stopPrice. up: Triggers when the price reaches or goes above the stopPrice.
    take_profit_price: float  # price to trigger take-profit orders
    leverage: float = 1.0  # Leverage size of the order
    timestamp: Timestamp = Timestamp.utcnow()
    trigger_price: float | None = None  # The price a trigger order is triggered at
    reduce_only: bool = (
        False  # A mark to reduce the position size only. Set to False by default. Need to set the position size when reduceOnly is True.
    )
    time_in_force: str = "GTC"  # GTC, GTT, IOC, or FOK
    post_only: str | None = (
        None  # Post only flag, invalid when timeInForce is IOC or FOK
    )

    client_oid: str | None = None  # client order id, defaults to uuid if not passed
    remark: str | None = (
        None  # remark for the order, length cannot exceed 100 utf8 characters
    )
    stop_price_type: str = "MP"  # TP, IP or MP, defaults to MP: Mark Price
    close_order: bool = False  # set to True to close position
    test: bool = (
        False  # set to True to use the test order endpoint(does not submit order, use to validate params)
    )
    forceHold: bool = (
        False  # A mark to forcely hold the funds for an order, even though it's an order to reduce the position size. This helps the order stay on the order book and not get canceled when the position size changes. Set to False by default.
    )


@dataclass(frozen=True)
class CCTXExchangeConfig:
    name: str
    key: str
    secret: str
    ccxt_config: dict
    ccxt_async_config: dict
    pair_whitelist: list[str]
    pair_blacklist: list[str]
    password: str | None = None

    skip_pair_validation: bool = True


@dataclass(frozen=True)
class CCTXConfig:
    trading_mode: str
    exchange: CCTXExchangeConfig
    pairs: list
