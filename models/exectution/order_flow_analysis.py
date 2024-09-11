from numpy import std
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
        # Typical price: (high + low + close) / 3
        typical_price = (df["high"] + df["low"] + df["close"]) / 3

        # Calculate VWAP
        df["vwap"] = (typical_price * df["volume"]).cumsum() / df["volume"].cumsum()

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

        self._ohlcv = df

    def populate_orderbook_indicators(self):
        df = self.orderbook

        # Calculate bid-ask spread
        df["spread"] = df["ask_price"] - df["bid_price"]

        # Calculate order imbalance
        df["order_imbalance"] = df["bid_quantity"] - df["ask_quantity"]

        # Calculate cumulative order flow (COF)
        df["cumulative_order_flow"] = (df["bid_quantity"] - df["ask_quantity"]).cumsum()

        self._orderbook = df

    def populate_entry_signals(self):
        """
        Implements the scalping strategy using VWAP and order flow analysis.
        Returns a DataFrame with entry and exit signals.
        """

        # Entry Signal: Combining the conditions
        self._orderbook["entry_signal"] = (
            (self._orderbook["spread"] < self.spread_threshold)
            & (self._orderbook["order_imbalance"] > self.imbalance_threshold)
            & (self._orderbook["cumulative_order_flow"] > self.cof_threshold)
        )

        # Exit Signal: Opposite conditions for exit
        self._orderbook["exit_signal"] = (
            (self._orderbook["spread"] > self.spread_threshold)
            | (self._orderbook["order_imbalance"] < -self.imbalance_threshold)
            | (self._orderbook["cumulative_order_flow"].diff() < 0)
        )

        # Set the side of the trade based on VWAP and standard deviation band
        self._ohlcv["trade_side"] = ""
        self._ohlcv.loc[
            self._ohlcv["close"] < self._ohlcv["vwap_std_dev_lower_1"], "trade_side"
        ] = "long"
        self._ohlcv.loc[
            self._ohlcv["close"] > self._ohlcv["vwap_std_dev_upper_1"], "trade_side"
        ] = "short"

        # Set the risk based on the standard deviation band
        self._ohlcv["risk_pct"] = 0  # Initialize risk to 0
        self._ohlcv.loc[
            (self._ohlcv["close"] < self._ohlcv["vwap_std_dev_lower_1"]), "risk_pct"
        ] = 1  # 1% risk for lower 1 std deviation

        self._ohlcv.loc[
            (self._ohlcv["close"] < self._ohlcv["vwap_std_dev_lower_2"]), "risk_pct"
        ] = 2  # 2% risk for lower 2 std deviation

        self._ohlcv.loc[
            (self._ohlcv["close"] > self._ohlcv["vwap_std_dev_upper_1"]), "risk_pct"
        ] = 1  # 1% risk for upper 1 std deviation

        self._ohlcv.loc[
            (self._ohlcv["close"] > self._ohlcv["vwap_std_dev_upper_2"]), "risk_pct"
        ] = 2  # 2% risk for upper 2 std deviation
