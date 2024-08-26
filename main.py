# directory for executinga a strategy
import time
import logging

logging.basicConfig(filename="logs/bot_errors.log", level=logging.INFO)


class TradingBot:
    def __init__(self):
        self.api = ExchangeAPI()  # Initialize your exchange API
        self.strategy = Strategy()  # Initialize your trading strategy

    def run(self):
        while True:
            try:
                data = self.api.get_market_data()  # Get real-time market data
                signal = self.strategy.generate_signal(
                    data
                )  # Process data and generate a signal

                if signal == "BUY":
                    self.api.execute_trade("BUY")
                    logging.info("Executed BUY order")
                elif signal == "SELL":
                    self.api.execute_trade("SELL")
                    logging.info("Executed SELL order")

                time.sleep(1)  # Sleep or wait for the next data tick

            except Exception as e:
                logging.error(f"Error: {e}")
                time.sleep(5)  # Wait before retrying


if __name__ == "__main__":
    bot = TradingBot()
    bot.run()
