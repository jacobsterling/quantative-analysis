import logging
from functools import reduce

import talib.abstract as ta
from pandas import DataFrame
from technical import qtpylib
import numpy as np
from freqtrade.strategy import CategoricalParameter, IStrategy


logger = logging.getLogger(__name__)


class TrendMomoRegression(IStrategy):

    minimal_roi = {"0": 0.1, "240": -1}

    plot_config = {
        "main_plot": {},
        "subplots": {
            "&-s_close": {"prediction": {"color": "blue"}},
            "do_predict": {
                "do_predict": {"color": "brown"},
            },
        },
    }

    process_only_new_candles = True
    stoploss = -0.05
    use_exit_signal = True
    startup_candle_count: int = 40
    can_short = True

    std_dev_multiplier_buy = CategoricalParameter(
        [0.75, 1, 1.25, 1.5, 1.75], default=1.25, space="buy", optimize=True)
    std_dev_multiplier_sell = CategoricalParameter(
        [0.75, 1, 1.25, 1.5, 1.75], space="sell", default=1.25, optimize=True)

    def feature_engineering_expand_all(self, df: DataFrame, period, **kwargs):

        df[["%-stoch_rsi_K-period", "%-stoch_rsi_D-period"]] = ta.STOCHRSI(
            df, timeperiod=period)[["fastk", "fastd"]]

        mfv = ((df['close'] - df['low']) - (df['high'] - df['close'])
               ) / (df['high'] - df['low']) * df['volume']

        df["%-A/D-period"] = mfv.rolling(period).sum()

        df["%-relative_volume-period"] = (df["volume"] /
                                          df["volume"].rolling(period).mean())

        return df

    def feature_engineering_expand_basic(self, df: DataFrame, **kwargs):

        df["%-pct-change"] = df["close"].pct_change()
        df["%-raw_volume"] = df["volume"]
        df["%-raw_price"] = df["close"]
        return df

    def feature_engineering_standard(self, df: DataFrame, **kwargs):

        df["%-day_of_week"] = df["date"].dt.dayofweek
        df["%-hour_of_day"] = df["date"].dt.hour

        return df

    def set_freqai_targets(self, df: DataFrame, **kwargs):

        df["&-s_close"] = (
            df["close"]
            .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
            .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
            .mean()
            / df["close"]
            - 1
        )

        # df['&s-up_or_down'] = np.where(df["close"].shift(-50) >
        #                                       df["close"], 'up', 'down')

        return df

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:

        df = self.freqai.start(df, metadata, self)

        for val in self.std_dev_multiplier_buy.range:
            df[f'target_roi_{val}'] = (
                df["&-s_close_mean"] + df["&-s_close_std"] * val
            )
        for val in self.std_dev_multiplier_sell.range:
            df[f'sell_roi_{val}'] = (
                df["&-s_close_mean"] - df["&-s_close_std"] * val
            )
        return df

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:

        enter_long_conditions = [
            df["do_predict"] == 1,
            df["&-s_close"] > df[f"target_roi_{self.std_dev_multiplier_buy.value}"],
        ]

        if enter_long_conditions:
            df.loc[
                reduce(lambda x, y: x & y, enter_long_conditions), [
                    "enter_long", "enter_tag"]
            ] = (1, "long")

        enter_short_conditions = [
            df["do_predict"] == 1,
            df["&-s_close"] < df[f"sell_roi_{self.std_dev_multiplier_sell.value}"],
        ]

        if enter_short_conditions:
            df.loc[
                reduce(lambda x, y: x & y, enter_short_conditions), [
                    "enter_short", "enter_tag"]
            ] = (1, "short")

        return df

    def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        exit_long_conditions = [
            df["do_predict"] == 1,
            df["&-s_close"] < df[f"sell_roi_{self.std_dev_multiplier_sell.value}"] * 0.25,
        ]
        if exit_long_conditions:
            df.loc[reduce(lambda x, y: x & y, exit_long_conditions),
                   "exit_long"] = 1

        exit_short_conditions = [
            df["do_predict"] == 1,
            df["&-s_close"] > df[f"target_roi_{self.std_dev_multiplier_buy.value}"] * 0.25,
        ]
        if exit_short_conditions:
            df.loc[reduce(lambda x, y: x & y,
                          exit_short_conditions), "exit_short"] = 1

        return df

    def get_ticker_indicator(self):
        return int(self.config["timeframe"][:-1])

    def confirm_trade_entry(
        self,
        pair: str,
        order_type: str,
        amount: float,
        rate: float,
        time_in_force: str,
        current_time,
        entry_tag,
        side: str,
        **kwargs,
    ) -> bool:

        df, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = df.iloc[-1].squeeze()

        if side == "long":
            if rate > (last_candle["close"] * (1 + 0.0025)):
                return False
        else:
            if rate < (last_candle["close"] * (1 - 0.0025)):
                return False

        return True
