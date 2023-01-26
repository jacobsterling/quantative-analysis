import backtrader as bt
import joblib
import numpy as np
from pathlib import Path

AGENTS_path = Path(r"F://AiQuant/models")

# trained using RSI (known as a lagging indicator and accurate in hindsight)
# confirmation using 36 length bollinger bands targeting mid point (36 ema)
# should work best on 1h tf
# needs more training


class LogReg(bt.Strategy):
    # stop and risk in %, symbol is what agent to load
    params = {'percents': 1, 'symbol': '^GSPC',  "period": 36, "devfactor": 2}

    def __init__(self):
        self.boll = bt.indicators.BollingerBands(
            period=self.params.period, devfactor=self.params.devfactor)

        AGENT_path = AGENTS_path / f'{self.params.symbol}-agent.pkl'

        model = joblib.load(AGENT_path)

        data = np.column_stack(
            [self.datas[0].open, self.datas[0].high, self.datas[0].low, self.datas[0].close])

        self.predictions = model.predict(data)

        self.idx = 0

    def next(self):
        if self.position:
            if self.position.size > 0:
                self.sell(exectype=bt.Order.Limit,
                          price=self.boll.lines.mid[0])

            else:
                self.buy(exectype=bt.Order.Limit,
                         price=self.boll.lines.mid[0])

        else:
            if self.predictions[self.idx] == 1:
                if self.data.close > self.boll.lines.top:
                    self.sell(exectype=bt.Order.Stop,
                              price=self.boll.lines.top[0])

                if self.data.close < self.boll.lines.bot:
                    self.buy(exectype=bt.Order.Stop,
                             price=self.boll.lines.bot[0])

        self.idx += 1
