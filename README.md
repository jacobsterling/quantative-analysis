## What is FreqTrade?

FreqTrade is a free and open-source crypto trading bot written in Python. It is designed to support all major exchanges and be controlled via Telegram or through its built-in webserver. Some key features of FreqTrade include:

- Backtesting and hyperopt (optimization) capabilities
- Extensible strategy framework
- Edge positioning
- Whitelist and blacklist configuration
- Live trading and dry-run (simulation) modes
- Telegram integration for easy control and monitoring

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/jacobsterling/quantitative-analysis.git
   cd quantitative-analysis
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the root directory and add your API credentials:
   ```
   TV_USERNAME=your_tradingview_username
   TV_PASSWORD=your_tradingview_password
   ```

## FreqTrade Setup

1. Install FreqTrade dependencies:
   ```
   pip install freqtrade
   ```

2. Initialize FreqTrade configuration:
   ```
   freqtrade create-userdir --userdir user_data
   ```

3. Create a new configuration file:
   ```
   freqtrade new-config --config user_data/config.json
   ```

4. Edit the `user_data/config.json` file to set up your exchange API keys, trading pairs, and other preferences.

5. Create a new strategy:
   ```
   freqtrade new-strategy --strategy MyAwesomeStrategy
   ```

6. Edit the strategy file in `user_data/strategies/MyAwesomeStrategy.py` to implement your trading logic.

## Usage

### Running Strategies

To run a strategy, use the Jupyter notebooks provided in the `notebooks/` directory. For example:

```
jupyter notebook notebooks/strategy_example.ipynb
```

### Analyzing Options

For options analysis, refer to the notebooks in `notebooks/black_scholes/`:

- `pricing_model.ipynb`: Black-Scholes option pricing
- `volatility_surface_analysis.ipynb`: Volatility surface visualization

### Order Flow Analysis

Use the `notebooks/order_heat_map.ipynb` notebook to visualize order flow and market depth.

### Running FreqTrade

To start FreqTrade with your custom strategy:

```
freqtrade trade -c user_data/config.json -s StrategyName
```

For backtesting:

```
freqtrade backtesting -c user_data/config.json -s StrategyName --timerange 20210101-20210331
```

## Project Structure

- `data_lib/`: Data fetching and processing utilities
- `strategies/`: FreqTrade Trading strategy implementations
- `notebooks/`: Jupyter notebooks for analysis and visualization
- `docker-compose.yml`: Docker configuration for running the project
- `user_data/`: FreqTrade user data directory
  - `strategies/`: Custom FreqTrade strategies
  - `config.json`: FreqTrade configuration file

## FreqTrade Documentation

For more detailed information on using FreqTrade, please refer to the official documentation:

- [FreqTrade Documentation](https://www.freqtrade.io/en/stable/)
- [Strategy Customization](https://www.freqtrade.io/en/stable/strategy-customization/)
- [Configuration](https://www.freqtrade.io/en/stable/configuration/)
- [Backtesting](https://www.freqtrade.io/en/stable/backtesting/)
- [Hyperopt](https://www.freqtrade.io/en/stable/hyperopt/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.