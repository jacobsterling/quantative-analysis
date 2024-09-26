from pathlib import Path

# Base project directory
PROJECT_ROOT = Path(__file__).parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
BACKTEST_RESULTS_DIR = PROJECT_ROOT / "backtest_results"

# Model directories
MODEL_DIR = PROJECT_ROOT / "freqaimodels"

# Config files
CONFIG_DIR = PROJECT_ROOT / "config.json"
CONFIGURATION_DIR = PROJECT_ROOT / "configuration"

# Results and output
TRADES_DB_FILE = PROJECT_ROOT / "tradesv3.sqlite"

LOGS_DIR = PROJECT_ROOT / "logs"

DB_URL = "sqlite:////freqtrade/user_data/tradesv3.sqlite"


def get_model_path(model_name: str) -> Path:
    """Get the full path for a trained model."""
    return MODEL_DIR / f"{model_name}.pkl"
