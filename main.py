import json
import sys
from dotenv import load_dotenv
from configuration.server import TELEGRAM_CONFIG, API_SERVER_CONFIG
from configuration.pairlists import PAIRLIST_DEFAULT
from configuration.exchanges import get_exchange_config
from configuration.execution import (
    ENTRY_PRICING,
    EXIT_PRICING,
    UNFILLED_TIMEOUT,
    RESTRICTIONS,
)
from constants import DB_URL

# Load environment variables from .env file
load_dotenv(".env")


def generate_config(exchange: str):
    config = {
        "$schema": "https://schema.freqtrade.io/schema.json",
        "fiat_display_currency": "USD",
        **RESTRICTIONS,
        "unfilledtimeout": UNFILLED_TIMEOUT,
        "entry_pricing": ENTRY_PRICING,
        "exit_pricing": EXIT_PRICING,
        "exchange": get_exchange_config(exchange),
        "pairlists": PAIRLIST_DEFAULT,
        "telegram": TELEGRAM_CONFIG,
        "api_server": API_SERVER_CONFIG,
        "bot_name": "freqtrade",
        "db_url": DB_URL,
        "initial_state": "running",
        "internals": {"process_throttle_secs": 5},
    }

    with open("/freqtrade/config.json", "w") as f:
        json.dump(config, f, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_config.py <exchange>")
        sys.exit(1)

    exchange = sys.argv[1]
    generate_config(exchange)
