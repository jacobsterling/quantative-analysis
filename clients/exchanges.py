from .config import CCTXExchangeConfig
from ccxt import Exchange, kucoinfutures


class KucoinFutures:

    ctx: Exchange
    config = CCTXExchangeConfig

    def __init__(self, exchange_config: CCTXExchangeConfig):
        self.ctx = kucoinfutures(
            {
                "apiKey": CCTXExchangeConfig.key,
                "secret": CCTXExchangeConfig.secret,
                "password": CCTXExchangeConfig.password,
            }
        )
        self.config = CCTXExchangeConfig
