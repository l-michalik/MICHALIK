import os

from v2.utils.main import read_csv_to_dicts, save_pickle
from v2.utils.main import extract_zip
from typing import List, Dict

def process_train_data(filepath: str) -> None:
    data = read_csv_to_dicts(filepath)
    data.reverse()
    save_pickle(data, 'train_data.pickle')

def process_test_data(filepath: str) -> None:
    data = read_csv_to_dicts(filepath)
    save_pickle(data, 'test_data.pickle')

def process_store_data(store_path: str, state_path: str) -> None:
    store_data = read_csv_to_dicts(store_path, fill_missing=True)
    state_data = read_csv_to_dicts(state_path)

    for store, state in zip(store_data, state_data):
        store['State'] = state.get('State', 'Unknown')

    save_pickle(store_data, 'store_data.pickle')

def extract_base() -> None:
    zip_path = 'data/zip/rossmann-store-sales.zip'
    extract_dir = './extracted'

    try:
        extract_zip(zip_path, extract_dir)
    except Exception as e:
        print(f"Error extracting zip: {e}")
        return

    files = {
        "train": ('train.csv', process_train_data),
        "test": ('test.csv', process_test_data),
        "store_combo": (('store.csv', 'store_states.csv'), process_store_data)
    }

    for key, (filenames, handler) in files.items():
        if isinstance(filenames, tuple):
            paths = [os.path.join(extract_dir, f) for f in filenames]
            if all(os.path.isfile(p) for p in paths):
                handler(*paths)
            else:
                print(f"Warning: missing one of {filenames}")
        else:
            path = os.path.join(extract_dir, filenames)
            if os.path.isfile(path):
                handler(path)
            else:
                print(f"Warning: {filenames} not found.")

if __name__ == '__main__':
    extract_base()
