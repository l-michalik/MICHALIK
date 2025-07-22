import logging
from preparing import prepare_dataset

logger = logging.getLogger(__name__)

def prepare() -> None:
    prepare_dataset()
    print("✅ prepare_dataset")
    
if __name__ == '__main__':
    prepare()