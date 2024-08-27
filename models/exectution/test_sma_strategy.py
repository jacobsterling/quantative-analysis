from . import ExecutionModel


class TestStrategy(ExecutionModel):
    def __init__(self, swindow: int, lwindow: int):
        super().__init__("TestSMAStrategy")
        self.__lwindow = lwindow
        self.__swindow = swindow

    def generate_signal(self, price_data):
        if len(price_data) < self.__lwindow:
            return "Hold"

        short_avg = sum(price_data[-self.__swindow :]) / self.__swindow
        long_avg = sum(price_data[-self.__lwindow :]) / self.__lwindow

        if short_avg > long_avg:
            return "Buy"
        elif short_avg < long_avg:
            return "Sell"
        else:
            return "Hold"

    @property
    def lwindow(self):
        return self.__lwindow

    @property
    def swindow(self):
        return self.__swindow
