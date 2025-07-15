from v2.extracting import extract_base, extract_weather, extract_google, extract_fbackward

def extracting() -> None:
    # extract_base()
    print('[1] extract_base')
    # extract_weather()
    print('[2] extract_weather')
    # extract_google()
    print('[3] extract_google')
    extract_fbackward()
    print('[4] extract_fbackward')

if __name__ == '__main__':
    extracting()