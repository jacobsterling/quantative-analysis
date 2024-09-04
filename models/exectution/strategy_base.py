from ccxt import Exchange, kucoinfutures
from clients.config import KUCOIN_CONFIG, Trade
from pandas import DataFrame, Timestamp, concat
from pytz import timezone
from clients.cctx.utils import fetch_orderbook, fetch_ohlcv


class ExecutionBase:

    ctx: kucoinfutures = kucoinfutures(
        {
            "apiKey": KUCOIN_CONFIG.key,
            "secret": KUCOIN_CONFIG.secret,
            "password": KUCOIN_CONFIG.password,
        }
    )

    _ohlcv: DataFrame = DataFrame(columns=["open", "high", "low", "close", "volume"])

    _orderbook: DataFrame = DataFrame(
        columns=[
            "bid_price",
            "bid_quantity",
            "ask_price",
            "ask_quantity",
            "symbol",
            "timestamp",
            "nonce",
        ]
    )

    def __init__(
        self,
        ticker: str,
        timeframe: str = "1m",
        from_date: Timestamp = Timestamp.now(
            tz=timezone("America/New_York")
        ).normalize(),
        load_order_book: bool = False,
    ):
        self.ticker = ticker
        if load_order_book:
            self.update_orderbook()

        self.timeframe = timeframe
        self.update_ohlcv(from_date)

    @property
    def orderbook(self) -> DataFrame:
        return self._orderbook

    @property
    def ohlcv(self) -> DataFrame:
        return self._ohlcv

    def update_orderbook(
        self,
    ):
        self._orderbook = fetch_orderbook(self.ctx, self.ticker)
        self.populate_orderbook_indicators(self)

    def update_ohlcv(
        self,
        since: Timestamp,
        limit: int = None,
        params: dict = {},
    ):

        data = fetch_ohlcv(self.ctx, self.ticker, self.timeframe, since, limit, params)

        self._ohlcv = concat([self._ohlcv, data], ignore_index=False)

        self.populate_indicators()

        return self._ohlcv

    def populate_indicators(self):
        return

    def populate_orderbook_indicators(self):
        return

    def populate_entry_signals(self):
        return

    def current_price(self):
        return self.ohlcv["close"].iloc[-1]

    def place_order(self, trade: Trade):

        self.ctx.create_order(
            Trade.symbol,
            "limit",
            Trade.side,
            trade.quantity,
            Trade.price,
            params={
                "triggerPrice": trade.trigger_price,
                "stopLossPrice": trade.stop_loss_price,
                "takeProfitPrice": trade.take_profit_price,
                "leverage": trade.leverage,
                "reduceOnly": trade.reduce_only,
                "timeInForce": trade.time_in_force,
                "postOnly": trade.post_only,
                "clientOid": trade.client_oid,
                "remark": trade.remark,
                "stop": trade.stop,
                "stopPriceType": trade.stop_price_type,
                "closeOrder": trade.close_order,
                "test": trade.test,
                "forceHold": trade.forceHold,
            },
        )
