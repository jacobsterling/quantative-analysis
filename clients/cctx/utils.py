from typing import Any
from pandas import DataFrame, Timestamp, concat
from ccxt import Exchange


def fetch_ohlcv(
    ctx: Exchange,
    ticker: str,
    timeframe: str,
    since: Timestamp,
    limit: int = None,
    params: dict[str, Any] = {},
):

    unix_since = int(since.timestamp() * 1000)

    data = DataFrame(
        ctx.fetch_ohlcv(ticker, timeframe, unix_since, limit, params),
        columns=["timestamp", "open", "high", "low", "close", "volume"],
    )

    data["timestamp"] = data["timestamp"].apply(Timestamp, unit="ms")

    return data.set_index("timestamp")


def fetch_orderbook(ctx: Exchange, ticker: str) -> DataFrame:

    ctx.load_markets()

    market = ctx.market(ticker)

    request = {
        "symbol": market["id"],
    }
    response = ctx.safe_value(ctx.futuresPublicGetLevel2Snapshot(request), "data", {})

    bids = DataFrame(
        ctx.parse_bids_asks(
            response.get("bids", []),
            0,
            1,
            2,
        ),
        columns=["bid_price", "bid_quantity"],
    ).sort_values(by="bid_price", ascending=False)

    asks = DataFrame(
        ctx.parse_bids_asks(
            response.get("asks", []),
            0,
            1,
            2,
        ),
        columns=["ask_price", "ask_quantity"],
    ).sort_values(by="ask_price", ascending=True)

    orderbook = concat([bids, asks], axis=1)

    orderbook[["symbol", "timestamp", "nonce"]] = (
        ticker,
        Timestamp(
            ctx.parse_to_int(ctx.safe_integer(response, "ts") / 1000000),
            unit="ms",
        ),
        ctx.safe_value(response, "sequence", []),
    )

    return orderbook
