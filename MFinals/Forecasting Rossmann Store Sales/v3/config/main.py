from pathlib import Path

class Config:
    DATA_DIR = Path("temp")
    CSV_DIR = Path("temp/csv")
    JOBLIB_DIR = Path("temp/joblib")
    LOAD_SIZE = 10 # Number of rows to load at once OR None for all rows