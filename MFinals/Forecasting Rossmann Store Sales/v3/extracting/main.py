import logging
from v3.extracting import extract_base, extract_weather, extract_google, extract_forwardback

logger = logging.getLogger(__name__)

def extract() -> None:
    extract_base()
    print("[1] ✅")
    extract_weather()
    print("[2] ✅")
    extract_google()
    print("[3] ✅")
    extract_forwardback()
    print("[4] ✅")

if __name__ == '__main__':
    extract()