#!/bin/bash
EXCHANGE=${EXCHANGE:-binance}  # Default to binance if not set
python /freqtrade/main.py $EXCHANGE
freqtrade trade --strategy OrderFlowAnalysis --config /freqtrade/config.json --strategy-path /freqtrade/user_data/strategies --user-data-dir /freqtrade/user_data --dry-run --verbose

# backtesting --strategy OrderFlowAnalysis --config /freqtrade/config.json --timerange 20230101-20240101 --timeframe 1m --enable-protections --datadir /freqtrade/user_data/data
