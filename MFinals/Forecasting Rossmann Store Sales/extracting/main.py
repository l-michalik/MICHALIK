import logging
from extracting import extract_base, extract_weather, extract_google, extract_forwardback

logger = logging.getLogger(__name__)

def extract() -> None:
    extract_base()
    print("✅ extract_base")
    extract_weather()
    print("✅ extract_weather")
    extract_google()
    print("✅ extract_google")
    extract_forwardback()
    print("✅ extract_forwardback")

if __name__ == '__main__':
    extract()