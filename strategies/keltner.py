
import backtrader as bt
import yfinance as yf
import matplotlib

class Keltner(bt.Strategy):
    params = {'period': 36, 'stop': 3, 'percents': 1 } # stop and risk in %

    def __init__(self):
        self.ema = bt.indicators.ExponentialMovingAverage(period=self.params.period)
        self.atr = bt.indicators.AverageTrueRange(period=self.params.period)
        self.upper_stop_loss = self.ema + self.atr + self.atr * (self.params.stop / 100) 
        self.lower_stop_loss = self.ema - self.atr - self.atr * (self.params.stop / 100)

    def notify_order(self, order):
        if not order.status == order.Completed:
            return

        print(f'{  "Long" if order.isbuy() else "Short" } Position Opened @price: {order.executed.price}') if self.position else print(f'Position Closed @price: {order.executed.price}')
                
    def next(self):
        if not self.position:
            if self.data.close[0] > self.ema[0] - self.atr[0] and self.data.low[0] < self.ema[0] - self.atr[0]:
                self.buy(exectype=bt.Order.Market, stop=self.lower_stop_loss[0], limit=self.ema[0] )

            elif self.data.close[0] < self.ema[0] + self.atr[0] and self.data.low[0] > self.ema[0] + self.atr[0]:
                self.sell(exectype=bt.Order.Market, limit= self.ema[0], stop= self.upper_stop_loss[0] )

if __name__ == "__main__":
  cerebro = bt.Cerebro()

  data = yf.download("GC=F", interval="1m")

  feed = bt.feeds.PandasDirectData(dataname = data)

  cerebro.adddata(feed)

  cerebro.addstrategy(Keltner)

  cerebro.run()

  cerebro.plot(iplot=False, style="candlestick", volume = False, filename='plot.png' )
