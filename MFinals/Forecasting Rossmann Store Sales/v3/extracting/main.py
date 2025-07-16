import logging
from v3.extracting import extract_base, extract_weather, extract_google, extract_forwardback

logger = logging.getLogger(__name__)

def extract() -> None:
    extract_base()
    extract_weather()
    extract_google()
    extract_forwardback()

if __name__ == '__main__':
    extract()