import os
import csv
import glob
import pickle
from datetime import datetime
from typing import Dict, Tuple


def extract_state_code_from_filename(filename: str) -> str:
    """
    Extracts 2-letter state code from filename and maps special cases.
    """
    state = os.path.splitext(os.path.basename(filename))[0]
    state_code = state[-2:]
    if state_code == 'NI':
        return 'HB,NI'
    return state_code


def parse_trend_file(filepath: str, trend_data: Dict[Tuple[str, int, int], float]) -> None:
    """
    Parses a single CSV file with Google Trends data for one state,
    extracting (state_code, year, week) as key and normalized trend value as value.
    """
    state_code = extract_state_code_from_filename(filepath)

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)

        for row in reader:
            try:
                trend_value = int(row[1])
                end_date_str = row[0].split(' - ')[1]
                dt = datetime.strptime(end_date_str, '%Y-%m-%d')
                year, week = dt.year, dt.isocalendar()[1]

                key = (state_code, year, week)
                trend_data[key] = trend_value / 100
            except (IndexError, ValueError) as e:
                print(f"Skipping row in {filepath} due to error: {e}")
                continue


def save_google_trends_pickle(trends: Dict[Tuple[str, int, int], float], output_path: str = './pickles/google_trends.pickle') -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        pickle.dump(trends, f, protocol=pickle.HIGHEST_PROTOCOL)


def main() -> None:
    csv_dir = 'data/googletrend'
    trend_files = glob.glob(os.path.join(csv_dir, '*.csv'))

    if not trend_files:
        print(f"No trend CSV files found in directory: {csv_dir}")
        return

    google_trends = {}
    for file in trend_files:
        parse_trend_file(file, google_trends)

    save_google_trends_pickle(google_trends)


if __name__ == '__main__':
    main()
