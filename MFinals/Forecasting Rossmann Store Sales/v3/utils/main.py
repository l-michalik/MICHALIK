from pathlib import Path
from typing import List, Dict, Tuple
import csv
import zipfile
import logging
from joblib import dump
from datetime import datetime

from v3.constants.main import EVENT_CATEGORIES, STATE_ABBREVIATIONS

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
        data = list(reader)

    if fill_missing:
        for row in data:
            for key, value in row.items():
                if value == '':
                    row[key] = '0'
    return data

def save_joblib(data, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
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