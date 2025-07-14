import csv
import os
import pickle
import zipfile
from typing import List, Dict


def extract_zip(zip_path: str, extract_to: str) -> None:
    """
    Extracts a ZIP archive to a specified directory.
    """
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"ZIP file not found: {zip_path}")

    print(f"Extracting: {zip_path} → {extract_to}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("Extraction complete.\n")


def csv_to_dicts(csv_reader: csv.reader) -> List[Dict[str, str]]:
    """
    Converts a CSV reader into a list of dictionaries using the header row as keys.
    """
    keys = next(csv_reader, None)
    if keys is None:
        raise ValueError("CSV file is empty or missing a header row.")
    return [dict(zip(keys, row)) for row in csv_reader]


def fill_missing_with_string(data: List[Dict[str, str]], fill_value: str = '0') -> None:
    """
    Replaces empty string values in the dataset with a given fill value.
    """
    for row in data:
        for key in row:
            if row[key] == '':
                row[key] = fill_value


def save_as_pickle(filename: str, data) -> None:
    """
    Saves Python object to a pickle file in the './pickles/' directory.
    """
    os.makedirs('pickles', exist_ok=True)
    filepath = os.path.join('pickles', filename)

    with open(filepath, 'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Saved: {filepath}")


def process_train_data(filepath: str) -> None:
    """
    Processes the training data CSV and saves it as a pickle.
    """
    with open(filepath, newline='') as f:
        reader = csv.reader(f)
        data = csv_to_dicts(reader)
        data.reverse()
        save_as_pickle('train_data.pickle', data)


def process_test_data(filepath: str) -> None:
    """
    Processes the test data CSV and saves it as a pickle.
    """
    with open(filepath, newline='') as f:
        reader = csv.reader(f)
        data = csv_to_dicts(reader)
        save_as_pickle('test_data.pickle', data)


def process_store_data(store_path: str, state_path: str) -> None:
    """
    Processes store and store_states CSVs, merges them, and saves the result as a pickle.
    """
    with open(store_path, newline='') as store_file, open(state_path, newline='') as state_file:
        store_reader = csv.reader(store_file)
        state_reader = csv.reader(state_file)

        store_data = csv_to_dicts(store_reader)
        state_data = csv_to_dicts(state_reader)

        fill_missing_with_string(store_data)

        for i, store in enumerate(store_data):
            store['State'] = state_data[i].get('State', 'Unknown')

        save_as_pickle('store_data.pickle', store_data)


def main() -> None:
    zip_file_path = 'data/zip/rossmann-store-sales.zip'
    extract_dir = './extracted'

    try:
        extract_zip(zip_file_path, extract_dir)
    except Exception as e:
        print(f"Error extracting zip: {e}")
        return

    expected_files = {
        "train": os.path.join(extract_dir, 'train.csv'),
        "test": os.path.join(extract_dir, 'test.csv'),
        "store": os.path.join(extract_dir, 'store.csv'),
        "states": os.path.join(extract_dir, 'store_states.csv')
    }

    if os.path.exists(expected_files["train"]):
        process_train_data(expected_files["train"])
    else:
        print("Warning: train.csv not found.")

    if os.path.exists(expected_files["test"]):
        process_test_data(expected_files["test"])
    else:
        print("Warning: test.csv not found.")

    if os.path.exists(expected_files["store"]) and os.path.exists(expected_files["states"]):
        process_store_data(expected_files["store"], expected_files["states"])
    else:
        print("Warning: store.csv or store_states.csv not found.")

if __name__ == '__main__':
    main()
