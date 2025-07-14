import zipfile
import pickle
import csv
import os

from typing import List, Dict

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
    print(f"Saved: {filepath}")
