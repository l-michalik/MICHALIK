import os
import csv
import glob
from typing import Dict, Tuple, List, Set

from v2.utils.main import state_name_to_abbreviation, event_to_int, save_weather_pickle, normalize

def parse_weather_file(
    filepath: str,
    weather: Dict[Tuple[str, str], List[float]],
    events: Set[str]
) -> None:
    state_name = os.path.splitext(os.path.basename(filepath))[0]
    state_code = state_name_to_abbreviation(state_name)

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        headers = next(reader, None)
        if not headers:
            print(f"Skipping empty file: {filepath}")
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
                print(f"[{filepath}:{row_num}] Skipping invalid row: {e}")

def process_weather(csv_dir: str = 'data/weather') -> None:
    csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))

    if not csv_files:
        print(f"No CSV files found in directory: {csv_dir}")
        return

    weather_data: Dict[Tuple[str, str], List[float]] = {}
    observed_events: Set[str] = set()

    for filepath in csv_files:
        parse_weather_file(filepath, weather_data, observed_events)

    save_weather_pickle(weather_data)

if __name__ == '__main__':
    process_weather()
