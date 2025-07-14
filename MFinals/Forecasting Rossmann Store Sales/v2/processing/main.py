from v2.processing.unzip_data import unzip_data
from v2.processing.weather_processing import process_weather

def main() -> None:
    unzip_data()
    print('[1] Unzipped data successfully.')
    process_weather()
    print('[2] Processed weather data successfully.')

if __name__ == '__main__':
    main()