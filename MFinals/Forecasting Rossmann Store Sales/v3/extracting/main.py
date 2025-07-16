import logging
from v3.extracting import extract_base 

logger = logging.getLogger(__name__)

def extract() -> None:
    extract_base()
    print("[1] ✅")

if __name__ == '__main__':
    extract()