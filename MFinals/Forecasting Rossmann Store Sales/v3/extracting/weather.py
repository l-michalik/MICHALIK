import logging
import csv
from pathlib import Path
from typing import Dict, List, Set, Tuple

from v3.utils.main import normalize, event_to_int, state_name_to_abbreviation, save_joblib
from v3.config import Config

DATA_DIR = Config.DATA_DIR
JOBLIB_DIR = Config.JOBLIB_DIR

logger = logging.getLogger(__name__)

def parse_weather_file(
    filepath: Path,
    weather: Dict[Tuple[str, str], List[float]],
    events: Set[str]
) -> None:
    state_name = filepath.stem
    state_code = state_name_to_abbreviation(state_name)

    try:
        with filepath.open(newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            headers = next(reader, None)

            if not headers:
                logger.warning(f"Skipping empty file: {filepath}")
                return

            for row_num, row in enumerate(reader, start=2):
                try:
                    date = row[0]
                    key = (state_code, date)

                    temperature = [normalize(int(x), 10, 30) for x in row[1:4]]
                    humidity = [normalize(int(x), 50, 50) for x in row[7:10]]
                    wind = [int(row[16]) / 50, int(row[17]) / 30]
                    cloud = [int(row[20])] if row[20] != 'NA' else [0]
                    event_code = event_to_int(row[21])

                    events.add(row[21])
                    weather[key] = temperature + humidity + wind + cloud + [event_code]

                except (ValueError, IndexError) as e:
                    logger.warning(f"[{filepath}:{row_num}] Skipping invalid row: {e}")

    except Exception as e:
        logger.error(f"Failed to read file {filepath}: {e}")

def extract_weather() -> None:
    csv_dir = DATA_DIR / 'weather'
    csv_files = list(csv_dir.glob('*.csv'))

    if not csv_files:
        logger.warning(f"No CSV files found in directory: {csv_dir}")
        return

    weather_data: Dict[Tuple[str, str], List[float]] = {}
    observed_events: Set[str] = set()

    for filepath in csv_files:
        parse_weather_file(filepath, weather_data, observed_events)

    save_joblib(weather_data, JOBLIB_DIR / "weather.joblib")

if __name__ == "__main__":
    extract_weather()
