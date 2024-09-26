from freqtrade.strategy import IStrategy
from pandas import DataFrame
import numpy as np
import talib.abstract as ta


class OrderFlowAnalysis(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = "1m"

    # Define minimal ROI
    minimal_roi = {"60": 0.01, "30": 0.02, "0": 0.04}

    # Define stoploss
    stoploss = -0.10

    # Define trailing stoploss
    trailing_stop = False

    # Run "populate_indicators" only for new candle
    process_only_new_candles = True

    # These values can be overridden in the config
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Define threshold values for the signals
    spread_threshold = 0.5  # Example: a narrow spread threshold
    imbalance_threshold = 100  # Example: a positive imbalance threshold
    cof_threshold = 0  # Any positive cumulative order flow is good

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 200

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Calculate VWAP
        typical_price = (dataframe["high"] + dataframe["low"] + dataframe["close"]) / 3
        dataframe["vwap"] = (typical_price * dataframe["volume"]).cumsum() / dataframe[
            "volume"
        ].cumsum()

        # Calculate standard deviation of VWAP
        std_dev = np.std(dataframe["vwap"])

        # Upper and Lower std dev bands
        for i in range(1, 4):
            dataframe[f"vwap_std_dev_upper_{i}"] = dataframe["vwap"] + i * std_dev
            dataframe[f"vwap_std_dev_lower_{i}"] = dataframe["vwap"] - i * std_dev

        # Perform basic order flow analysis
        dataframe["order_flow"] = dataframe["close"].diff() * dataframe["volume"]
        dataframe["cumulative_delta"] = dataframe["order_flow"].cumsum()

        # Calculate bid-ask spread (assuming we have this data)
        if "bid" in dataframe.columns and "ask" in dataframe.columns:
            dataframe["spread"] = dataframe["ask"] - dataframe["bid"]

        # Calculate order imbalance (assuming we have this data)
        if "bid_size" in dataframe.columns and "ask_size" in dataframe.columns:
            dataframe["order_imbalance"] = dataframe["bid_size"] - dataframe["ask_size"]

        # Calculate cumulative order flow (COF)
        if "order_imbalance" in dataframe.columns:
            dataframe["cumulative_order_flow"] = dataframe["order_imbalance"].cumsum()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe.get("spread", 0) < self.spread_threshold)
                & (dataframe.get("order_imbalance", 0) > self.imbalance_threshold)
                & (dataframe.get("cumulative_order_flow", 0) > self.cof_threshold)
                & (dataframe["close"] < dataframe["vwap_std_dev_lower_1"])
            ),
            "enter_long",
        ] = 1

        dataframe.loc[
            (
                (dataframe.get("spread", 0) < self.spread_threshold)
                & (dataframe.get("order_imbalance", 0) < -self.imbalance_threshold)
                & (dataframe.get("cumulative_order_flow", 0) < -self.cof_threshold)
                & (dataframe["close"] > dataframe["vwap_std_dev_upper_1"])
            ),
            "enter_short",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        cof_condition = (
            dataframe["cumulative_order_flow"].diff() < 0
            if "cumulative_order_flow" in dataframe.columns
            else False
        )

        dataframe.loc[
            (
                (dataframe.get("spread", 0) > self.spread_threshold)
                | (dataframe.get("order_imbalance", 0) < -self.imbalance_threshold)
                | cof_condition
                | (dataframe["close"] > dataframe["vwap_std_dev_upper_1"])
            ),
            "exit_long",
        ] = 1

        cof_condition = (
            dataframe["cumulative_order_flow"].diff() > 0
            if "cumulative_order_flow" in dataframe.columns
            else False
        )

        dataframe.loc[
            (
                (dataframe.get("spread", 0) > self.spread_threshold)
                | (dataframe.get("order_imbalance", 0) > self.imbalance_threshold)
                | cof_condition
                | (dataframe["close"] < dataframe["vwap_std_dev_lower_1"])
            ),
            "exit_short",
        ] = 1

        return dataframe
