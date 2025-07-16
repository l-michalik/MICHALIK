import logging
from v3.extracting import extract_base, extract_weather

logger = logging.getLogger(__name__)

def extract() -> None:
    # extract_base()
    print("[1] ✅")
    extract_weather()
    print("[2] ✅")

if __name__ == '__main__':
    extract()