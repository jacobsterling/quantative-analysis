#!/bin/bash

# Set default exchange if not provided
EXCHANGE=${EXCHANGE:-binance}

# Generate config
echo "Generating config for exchange: $EXCHANGE"
python /freqtrade/main.py $EXCHANGE

# echo "Starting Freqtrade"
# freqtrade trade --config /freqtrade/config.json --strategy CVDDivergence

# echo "Running backtesting"
# freqtrade backtesting --strategy CVDDivergence --timerange 20240101-20240926 --timeframe 5m --max-open-trades 2 -p BTC/USDT:USDT --enable-protections --datadir /freqtrade/data

# echo "Running hyperopt"
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLossDaily --spaces buy --strategy CVDDivergence --datadir /freqtrade/data --max-open-trades 2 --timeframe 5m --timerange 20240101-20240926

# echo "Downloading data"
# freqtrade download-data --exchange $EXCHANGE --pairs ETH/USDT:USDT BTC/USDT:USDT --timeframe 5m --timerange 20240101-20240926 --trading-mode futures --datadir /freqtrade/data

echo "Downloading trade data"
freqtrade download-data -p BTC/USDT:USDT --timerange 20240101-20240926 --trading-mode futures --timeframes 5m --dl-trades
