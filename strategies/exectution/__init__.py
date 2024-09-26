class ExecutionModel:
    def __init__(self, strategy_name: str):
        self.__strategy_name = strategy_name

    def generate_signal(self, price_data):
        return "Hold"

    def name(self):
        return self.__strategy_name
