from v2.extracting import extract_base, extract_weather

def extracting() -> None:
    extract_base()
    print('[1] extract_base')
    extract_weather()
    print('[2] extract_weather')

if __name__ == '__main__':
    extracting()