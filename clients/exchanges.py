from .config import CCTXExchangeConfig, Trade, KUCOIN_CONFIG
from ccxt import Exchange, kucoinfutures
from pandas import Timestamp, DataFrame, concat, read_hdf
from pathlib import Path


class KucoinFutures:

    ctx: Exchange
    config: CCTXExchangeConfig

    def __init__(self, exchange_config: CCTXExchangeConfig = KUCOIN_CONFIG):
        self.ctx = kucoinfutures(
            {
                "apiKey": exchange_config.key,
                "secret": exchange_config.secret,
                "password": exchange_config.password,
            }
        )
        self.config = exchange_config
        self.data_path = Path("../data/kucoin/futures")
        if not self.data_path.exists():
            self.data_path.mkdir(parents=True)

    def get_balance(self):
        return self.ctx.fetch_balance()

    def load_market_data(
        self,
        symbol: str,
        data_type: str,
        timeframe: str | None = None,
    ):

        match data_type:
            case "ohlcv":
                return read_hdf(self.data_path / f"{symbol}_{data_type}_{timeframe}.h5")
            case "order_book":
                return read_hdf(self.data_path / f"{symbol}_{data_type}.h5")

    def save_market_data(
        self,
        symbol: str,
        data: DataFrame,
        data_type: str,
        timeframe: str | None = None,
    ):

        match data_type:
            case "ohlcv":

                data_path = self.data_path / f"{symbol}_{data_type}_{timeframe}.h5"

                if data_path.exists():
                    data = self.load_market_data(symbol, data_type, timeframe).append(
                        data
                    )

                data.to_hdf(data_path, key="data", mode="a")

            case "order_book":

                data_path = self.data_path / f"{symbol}_{data_type}.h5"

                if data_path.exists():
                    data = self.load_market_data(symbol, data_type).append(data)

                data.to_hdf(data_path, key="data", mode="a")

        data.to_hdf(f"../data/kucoin/futures/{data_type}", key="data", mode="a")

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        since: Timestamp,
        limit: int = None,
        params: dict = {},
    ) -> DataFrame:

        unix_since = int(since.timestamp() * 1000)

        data = DataFrame(
            self.ctx.fetch_ohlcv(symbol, timeframe, unix_since, limit, params),
            columns=["timestamp", "open", "high", "low", "close", "volume"],
        )

        data["timestamp"] = data["timestamp"].apply(Timestamp, unit="ms")

        return data.set_index("timestamp")

    def fetch_order_book(self, symbol: str) -> DataFrame:

        self.ctx.load_markets()
        market = self.ctx.market(symbol)

        request = {
            "symbol": market["id"],
        }
        response = self.ctx.safe_value(
            self.ctx.futuresPublicGetLevel2Snapshot(request), "data", {}
        )

        bids = DataFrame(
            self.ctx.parse_bids_asks(
                response.get("bids", []),
                0,
                1,
                2,
            ),
            columns=["bid_price", "bid_quantity"],
        ).sort_values(by="bid_price", ascending=False)

        asks = DataFrame(
            self.ctx.parse_bids_asks(
                response.get("asks", []),
                0,
                1,
                2,
            ),
            columns=["ask_price", "ask_quantity"],
        ).sort_values(by="ask_price", ascending=True)

        orderbook = concat([bids, asks], axis=1)

        orderbook[["symbol", "timestamp", "nonce"]] = (
            symbol,
            Timestamp(
                self.ctx.parse_to_int(self.ctx.safe_integer(response, "ts") / 1000000),
                unit="ms",
            ),
            self.ctx.safe_value(response, "sequence", []),
        )

        return orderbook

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
