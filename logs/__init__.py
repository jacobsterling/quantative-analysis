from pandas import DataFrame, read_excel


def _get_trade_log() -> DataFrame:

    log = read_excel("trade_log.xlsx")

    yield log

    log.to_excel("trade_log.xlsx", index=False)


def log_trade(trade):
    log = _get_trade_log()
    log = log.append(trade, ignore_index=True)
