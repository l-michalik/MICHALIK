import zipfile
import pickle
import csv
import os

from typing import List, Dict, Tuple
from v2.consts import EVENT_CATEGORIES, STATE_ABBREVIATIONS

def extract_zip(zip_path: str, extract_to: str) -> None:
    if not os.path.isfile(zip_path):
        raise FileNotFoundError(f"ZIP file not found: {zip_path}")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def read_csv_to_dicts(filepath: str, fill_missing: bool = False) -> List[Dict[str, str]]:
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    if fill_missing:
        for row in data:
            for k, v in row.items():
                if v == '':
                    row[k] = '0'
    return data

def save_pickle(data, filename: str, dir_: str = 'pickles') -> None:
    os.makedirs(dir_, exist_ok=True)
    filepath = os.path.join(dir_, filename)
    with open(filepath, 'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    
def normalize(value: int, offset: int, scale: int) -> float:
    return (value - offset) / scale

def event_to_int(event: str) -> int:
    try:
        return EVENT_CATEGORIES.index(event)
    except ValueError:
        return 0

def state_name_to_abbreviation(state_name: str) -> str:
    return STATE_ABBREVIATIONS.get(state_name, 'UNKNOWN')

def save_weather_pickle(
    weather: Dict[Tuple[str, str], List[float]],
    output_path: str = './pickles/weather.pickle'
) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        pickle.dump(weather, f, protocol=pickle.HIGHEST_PROTOCOL)