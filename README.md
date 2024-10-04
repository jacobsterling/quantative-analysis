# Quantitative Analysis Notebooks

Welcome to the notebooks directory of our Quantitative Analysis and Strategy Creation project. This folder contains Jupyter notebooks that demonstrate various financial strategies, analyses, and backtesting results.

## Directory Structure

```
notebooks/
├── back_testing/
│   ├── strategy_analysis_example.ipynb
│   └── CVDDivergence_analysis.ipynb
├── black_scholes/
│   └── hedging_strategies.ipynb
├── kucoin_futures_pairs_analysis.ipynb
├── order_heat_map.ipynb
├── portfolio_analysis.ipynb
└── trade_analysis.ipynb
```

## Notebook Descriptions

### Back Testing

The `back_testing/` directory contains notebooks that utilize algorithms from the [jacobsterling/trading-algorithms](https://github.com/jacobsterling/trading-algorithms) repository. These notebooks demonstrate the implementation and analysis of various trading strategies:

- `strategy_analysis_example.ipynb`: A general example of strategy analysis using the backtesting framework.
- `CVDDivergence_analysis.ipynb`: Analysis of the Cumulative Volume Delta (CVD) Divergence strategy.

### Black-Scholes

- `hedging_strategies.ipynb`: Explores option pricing and hedging strategies using the Black-Scholes model.

### Other Analyses

- `kucoin_futures_pairs_analysis.ipynb`: Analysis of futures trading pairs on the KuCoin exchange.
- `order_heat_map.ipynb`: Visualization of order book data using heat maps.
- `portfolio_analysis.ipynb`: In-depth analysis of portfolio performance and risk metrics.
- `trade_analysis.ipynb`: Detailed examination of individual trades and their outcomes.

## Usage

To use these notebooks:

1. Ensure you have Jupyter Notebook or JupyterLab installed.
2. Navigate to this directory in your terminal.
3. Run `jupyter notebook` or `jupyter lab` to start the Jupyter server.
4. Open the desired notebook to view, run, or modify the analyses.

## Dependencies

These notebooks rely on various Python libraries for data analysis and visualization. Ensure you have installed all dependencies listed in the project's `requirements.txt` file.

## Contributing

We welcome contributions to enhance these notebooks or add new analyses. Please refer to the main project README for contribution guidelines.

## License

This project is licensed under the MIT License. See the LICENSE file in the root directory for details.