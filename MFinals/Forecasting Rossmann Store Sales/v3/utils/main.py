from pathlib import Path
from typing import List, Dict
import csv
import zipfile
import logging
from joblib import dump

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
