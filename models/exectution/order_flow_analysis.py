from pandas import DataFrame
from numpy import std
from ta.volume import VolumeWeightedAveragePrice
from .strategy_base import ExecutionBase


class OrderFlowAnalysis(ExecutionBase):

    # Define threshold values for the signals
    spread_threshold = 0.5  # Example: a narrow spread threshold
    imbalance_threshold = 100  # Example: a positive imbalance threshold
    cof_threshold = 0  # Any positive cumulative order flow is good

    def populate_indicators(self):
        df = self.ohlcv
        """
        Calculate the VWAP for the given data.
        """
        vwap = VolumeWeightedAveragePrice(
            high=df["high"], low=df["low"], close=df["close"], volume=df["volume"]
        )
        df["vwap"] = vwap.volume_weighted_average_price()

        # Calculate standard deviation of VWAP
        std_dev = std(df["vwap"])

        # Upper and Lower std dev bands
        for i in range(1, 4):
            df[f"vwap_std_dev_upper_{i}"] = df["vwap"] + i * std_dev
            df[f"vwap_std_dev_lower_{i}"] = df["vwap"] - i

        """
        Perform a basic order flow analysis.
        This is a simplified version using the cumulative delta of the close price.
        More sophisticated methods might involve tick data or order book analysis.
        """
        df["order_flow"] = (
            df["close"].diff() * df["volume"]
        )  # Proxy for buy/sell pressure
        df["cumulative_delta"] = df["order_flow"].cumsum()  # Cumulative delta

        # # Calculate VWAP rate of change
        # df["vwap_roc"] = df["vwap"].pct_change()

        # # Calculate order flow rate of change
        # df["order_flow_roc"] = df["order_flow"].pct_change()

        # # Calculate order flow momentum
        # df["order_flow_momentum"] = df["order_flow"].rolling(window=5).mean()

        # # Calculate order flow volatility
        # df["order_flow_volatility"] = df["order_flow"].rolling(window=10).std()

        self.ohlcv = df

    def populate_orderbook_indicators(self):
        df = self.orderbook

        # Calculate bid-ask spread
        df["spread"] = df["ask_price"] - df["bid_price"]

        # Calculate order imbalance
        df["order_imbalance"] = df["bid_quantity"] - df["ask_quantity"]

        # Calculate cumulative order flow (COF)
        df["cumulative_order_flow"] = (df["bid_quantity"] - df["ask_quantity"]).cumsum()

        self.orderbook = df

    def populate_entry_signals(self):
        """
        Implements the scalping strategy using VWAP and order flow analysis.
        Returns a DataFrame with entry and exit signals.
        """

        df = self.orderbook

        # Entry Signal: Combining the conditions
        df["entry_signal"] = (
            (df["spread"] < self.spread_threshold)
            & (df["order_imbalance"] > self.imbalance_threshold)
            & (df["cumulative_order_flow"] > self.cof_threshold)
        )

        # Exit Signal: Opposite conditions for exit
        df["exit_signal"] = (
            (df["spread"] > self.spread_threshold)
            | (df["order_imbalance"] < -self.imbalance_threshold)
            | (df["cumulative_order_flow"].diff() < 0)
        )

        self.orderbook = df
