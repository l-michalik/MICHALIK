import logging
from pathlib import Path
from typing import Dict, Tuple

from v3.utils.main import parse_trend_file, save_joblib
from v3.config import Config

DATA_DIR = Config.DATA_DIR
JOBLIB_DIR = Config.JOBLIB_DIR

logger = logging.getLogger(__name__)

def extract_google(csv_dir: Path = Path("data/googletrend")) -> None:
    csv_dir = DATA_DIR / 'google'
    trend_files = list(csv_dir.glob("*.csv"))

    if not trend_files:
        logger.warning(f"No trend CSV files found in directory: {csv_dir}")
        return

    trends: Dict[Tuple[str, int, int], float] = {}

    for file in trend_files:
        parse_trend_file(file, trends)

    save_joblib(trends, JOBLIB_DIR / "google.joblib")


if __name__ == "__main__":
    extract_google()
