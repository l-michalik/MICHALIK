from pathlib import Path
from typing import List, Dict, Tuple
import csv
import zipfile
import logging
from joblib import dump
import numpy as np
import pandas as pd
from datetime import datetime
from isoweek import Week
import math
from config.main import Config
import itertools

LOAD_SIZE = Config.LOAD_SIZE

from constants.main import EVENT_CATEGORIES, STATE_ABBREVIATIONS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def extract_zip(zip_path: Path, extract_to: Path) -> None:
    if not zip_path.is_file():
        raise FileNotFoundError(f"ZIP file not found: {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    logger.info(f"Extracted {zip_path} to {extract_to}")

def read_csv_to_dicts(filepath: Path, fill_missing: bool = False) -> List[Dict[str, str]]:
    with filepath.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(itertools.islice(reader, LOAD_SIZE))  # ograniczenie do LOAD_SIZE

    if fill_missing:
        for row in data:
            for key, value in row.items():
                if value == '':
                    row[key] = '0'
    return data

def read_csv_file(filepath: Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath, nrows=LOAD_SIZE, parse_dates=True)
        logger.info(f"Loaded CSV data from {filepath}")
        return df
    except Exception as e:
        logger.error(f"Failed to read CSV file {filepath}: {e}")
        raise

def save_joblib(data, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        # if isinstance(data, pd.DataFrame):
        #     data = data.head(LOAD_SIZE)
        # elif isinstance(data, list):
        #     data = data[:LOAD_SIZE]
        dump(data, path)
        logger.info(f"Saved data to {path}")
    except Exception as e:
        logger.exception(f"Failed to save data to {path}: {e}")

def normalize(value: int, offset: int, scale: int) -> float:
    return (value - offset) / scale

def event_to_int(event: str) -> int:
    try:
        return EVENT_CATEGORIES.index(event)
    except ValueError:
        return 0

def state_name_to_abbreviation(state_name: str) -> str:
    return STATE_ABBREVIATIONS.get(state_name, 'UNKNOWN')

def extract_state_code_from_filename(filename: str) -> str:
    state = Path(filename).stem
    state_code = state[-2:]
    return 'HB,NI' if state_code == 'NI' else state_code

def parse_trend_file(
    filepath: Path,
    trend_data: Dict[Tuple[str, int, int], float]
) -> None:
    state_code = extract_state_code_from_filename(filepath)

    try:
        with filepath.open(newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)

            for row_num, row in enumerate(reader, start=2):
                try:
                    trend_value = int(row[1])
                    end_date_str = row[0].split(" - ")[1]
                    dt = datetime.strptime(end_date_str, "%Y-%m-%d")
                    year, week = dt.year, dt.isocalendar()[1]
                    trend_data[(state_code, year, week)] = trend_value / 100
                except (IndexError, ValueError) as e:
                    logger.warning(f"[{filepath}:{row_num}] Skipping row due to error: {e}")
    except Exception as e:
        logger.error(f"Failed to parse {filepath}: {e}")
        
import math
from datetime import datetime
from typing import Tuple, List, Dict, Any

from isoweek import Week


def abc2int(char: str) -> int:
    return {'0': 0, 'a': 1, 'b': 2, 'c': 3, 'd': 4}.get(char, 0)


def state2int(state: str) -> int:
    return {
        'HB,NI': 0, 'HH': 1, 'TH': 2, 'RP': 3, 'ST': 4,
        'BW': 5, 'SN': 6, 'BE': 7, 'HE': 8, 'SH': 9, 'BY': 10, 'NW': 11
    }.get(state, -1)


def promo_interval2int(interval: str) -> int:
    return {'0': 0, 'J': 1, 'F': 2, 'M': 3}.get(interval[0] if interval else '0', 0)


def has_competition_months(date: datetime, year: int, month: int) -> int:
    if year == 0:
        return 0
    open_date = datetime(year=year, month=month, day=15)
    delta_months = (date - open_date).days // 30
    return max(0, min(delta_months, 24))


def has_promo2_weeks(date: datetime, year: int, week: int) -> int:
    if year == 0:
        return 0
    start_date = Week(year, week).monday()
    delta_weeks = (date.date() - start_date).days // 7
    return max(0, min(delta_weeks, 25))


def latest_promo2_months(date: datetime, interval: str, year: int, week: int) -> int:
    if not has_promo2_weeks(date, year, week):
        return 0
    month_code = promo_interval2int(interval)
    if month_code == 0:
        return 0
    if date.month < month_code:
        promo_year = date.year - 1
        promo_month = month_code + 9
    else:
        promo_year = date.year
        promo_month = ((date.month - month_code) // 3) * 3 + month_code
    promo_start = datetime(promo_year, promo_month, 1)
    return (date - promo_start).days // 30


def safe_int(val: Any, default=0) -> int:
    try:
        return int(val)
    except (ValueError, TypeError):
        return default

def transform_competition_year(years: np.ndarray) -> np.ndarray:
    years = years.copy()
    return np.where(years < 2000, 1, years - 1998)

def transform_promo2_year(years: np.ndarray) -> np.ndarray:
    years = years.copy()
    shifted = years - 2008
    return np.where(shifted < 0, 0, shifted)

def split_features(X: np.ndarray) -> list[np.ndarray]:
    X = np.asarray(X)
    X_list = [
        X[..., [1]] - 1,
        X[..., [2]] - 1,
        X[..., [3]],
        X[..., [4]] - 2013,
        X[..., [5]] - 1,
        X[..., [6]] - 1,
        X[..., [7]],
        X[..., [8]],
        X[..., [9]],
        X[..., [10]],
        X[..., [11]],
        X[..., [12]],
        X[..., [13]],
        X[..., [14]],
        X[..., [15]],
        transform_competition_year(X[..., [16]]),
        transform_promo2_year(X[..., [17]]),
        X[..., [18]],
        X[..., [19]] - 1,
        X[..., [20, 21, 22]],
        X[..., [23, 24, 25]],
        X[..., [26, 27]],
        X[..., [28]],
        X[..., [29]],
        X[..., [30]] - 1,
        X[..., [31]] - 1,
        X[..., [32]] - 1,
        X[..., [33]] - 1,
        X[..., [34]],
        X[..., [35]],
        X[..., [36]] - 1,
        X[..., [37]] - 1,
        X[..., [38]],
        X[..., [39]]
    ]
    return X_list
