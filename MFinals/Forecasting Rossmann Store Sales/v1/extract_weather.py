import os
import csv
import glob
import pickle
from typing import Dict, Tuple, List

def normalize(value: int, offset: int, scale: int) -> float:
    return (value - offset) / scale

def event_to_int(event: str) -> int:
    event_list = [
        '', 'Fog-Rain', 'Fog-Snow', 'Fog-Thunderstorm',
        'Rain-Snow-Hail-Thunderstorm', 'Rain-Snow', 'Rain-Snow-Hail',
        'Fog-Rain-Hail', 'Fog', 'Fog-Rain-Hail-Thunderstorm', 'Fog-Snow-Hail',
        'Rain-Hail', 'Rain-Hail-Thunderstorm', 'Fog-Rain-Snow', 'Rain-Thunderstorm',
        'Fog-Rain-Snow-Hail', 'Rain', 'Thunderstorm', 'Snow-Hail',
        'Rain-Snow-Thunderstorm', 'Snow', 'Fog-Rain-Thunderstorm'
    ]
    return event_list.index(event)

def state_name_to_abbreviation(state_name: str) -> str:
    mapping = {
        'BadenWuerttemberg': 'BW',
        'Bayern': 'BY',
        'Berlin': 'BE',
        'Brandenburg': 'BB',
        'Bremen': 'HB',
        'Hamburg': 'HH',
        'Hessen': 'HE',
        'MecklenburgVorpommern': 'MV',
        'Niedersachsen': 'HB,NI', 
        'NordrheinWestfalen': 'NW',
        'RheinlandPfalz': 'RP',
        'Saarland': 'SL',
        'Sachsen': 'SN',
        'SachsenAnhalt': 'ST',
        'SchleswigHolstein': 'SH',
        'Thueringen': 'TH'
    }
    return mapping.get(state_name, 'UNKNOWN')

def parse_weather_file(filepath: str, weather: Dict[Tuple[str, str], List[float]], events_set: set) -> None:
    state_name = os.path.splitext(os.path.basename(filepath))[0]
    state_code = state_name_to_abbreviation(state_name)

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        headers = next(reader, None)
        if headers is None:
            print(f"Skipping empty file: {filepath}")
            return

        for row in reader:
            try:
                date = row[0]
                key = (state_code, date)

                temp_raw = list(map(int, row[1:4]))
                temperature = [normalize(x, 10, 30) for x in temp_raw]

                humidity_raw = list(map(int, row[7:10]))
                humidity = [normalize(x, 50, 50) for x in humidity_raw]

                wind = [int(row[16]) / 50, int(row[17]) / 30]

                cloud = [int(row[20])] if row[20] != 'NA' else [0]
                event_code = event_to_int(row[21])
                events_set.add(row[21])

                weather[key] = temperature + humidity + wind + cloud + [event_code]
            except (ValueError, IndexError) as e:
                print(f"Error parsing row in {filepath}: {e}")
                continue


def save_weather_pickle(weather: Dict[Tuple[str, str], List[float]], output_path: str = './pickles/weather.pickle') -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        pickle.dump(weather, f, protocol=pickle.HIGHEST_PROTOCOL)

def main():
    csv_dir = 'data/weather'
    csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))

    if not csv_files:
        print(f"No CSV files found in directory: {csv_dir}")
        return

    weather_data = {}
    observed_events = set()

    for csv_file in csv_files:
        parse_weather_file(csv_file, weather_data, observed_events)

    save_weather_pickle(weather_data)

if __name__ == '__main__':
    main()
