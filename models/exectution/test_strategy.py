from . import ExecutionModel


class TestStrategy(ExecutionModel):
    def __init__(self, long_window: int, short_window: int):
        super().__init__("TestStrategy")
        self.long_window = long_window
        self.short_window = short_window
