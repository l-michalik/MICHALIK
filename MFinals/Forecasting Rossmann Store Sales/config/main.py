from pathlib import Path

class Config:
    DATA_DIR = Path("data")
    CSV_DIR = Path("temp/csv")
    JOBLIB_DIR = Path("temp/joblib")
    LOAD_SIZE = None # Number of rows to load at once OR None for all rows