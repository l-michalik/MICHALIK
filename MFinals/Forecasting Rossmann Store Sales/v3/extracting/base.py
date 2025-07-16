import logging
from pathlib import Path
from typing import Callable, Union

from v3.utils.main import extract_zip, read_csv_to_dicts, save_joblib
from v3.config import Config

OUTPUT_DIR = Config.OUTPUT_DIR
DATA_DIR = Config.DATA_DIR
EXTRACT_DIR = Config.EXTRACT_DIR

logger = logging.getLogger(__name__)

def process_train_data(filepath: Path) -> None:
    data = read_csv_to_dicts(filepath)
    data.reverse()
    save_joblib(data, OUTPUT_DIR / "train_data.joblib")

def process_test_data(filepath: Path) -> None:
    data = read_csv_to_dicts(filepath)
    save_joblib(data, OUTPUT_DIR / "test_data.joblib")

def process_store_data(store_path: Path, state_path: Path) -> None:
    store_data = read_csv_to_dicts(store_path, fill_missing=True)
    state_data = read_csv_to_dicts(state_path)

    for store, state in zip(store_data, state_data):
        store["State"] = state.get("State", "Unknown")

    save_joblib(store_data, OUTPUT_DIR / "store_data.joblib")

def extract_base() -> None:
    zip_path = DATA_DIR / "rossmann-store-sales.zip"

    try:
        extract_zip(zip_path, EXTRACT_DIR)
    except Exception as e:
        logger.error(f"Error extracting zip file: {e}")
        return

    tasks: dict[str, tuple[Union[str, tuple[str, str]], Callable]] = {
        "train": ("train.csv", process_train_data),
        "test": ("test.csv", process_test_data),
        "store_combo": (("store.csv", "store_states.csv"), process_store_data),
    }

    for label, (files, handler) in tasks.items():
        if isinstance(files, tuple):
            paths = [EXTRACT_DIR / f for f in files]
            if all(p.exists() for p in paths):
                handler(*paths)
            else:
                logger.warning(f"Missing one or more files for {label}: {files}")
        else:
            path = EXTRACT_DIR / files
            if path.exists():
                handler(path)
            else:
                logger.warning(f"Missing file for {label}: {files}")

if __name__ == "__main__":
    extract_base()
