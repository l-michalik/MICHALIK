import os
import zipfile
from abc import ABC, abstractmethod
import pandas as pd

class DataIngestor(ABC):
    @abstractmethod
    def ingest(self, file_path: str) -> list[pd.DataFrame]:
        pass

class ZipDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> list[pd.DataFrame]:
        if not file_path.endswith(".zip"):
            raise ValueError("Invalid file type")

        extract_dir = "extracted_data"
        if os.path.exists(extract_dir):
            for root, dirs, files in os.walk(extract_dir, topdown=False):
                for f in files:
                    os.remove(os.path.join(root, f))
                for d in dirs:
                    os.rmdir(os.path.join(root, d))
            os.rmdir(extract_dir)

        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        train_csv_path = None
        for root, _, files in os.walk(extract_dir):
            for f in files:
                if f == "train.csv":
                    train_csv_path = os.path.join(root, f)
                    break
            if train_csv_path:
                break

        if not train_csv_path:
            raise FileNotFoundError("train.csv not found in the zip archive")

        df = None
        for encoding in ["utf-8", "ISO-8859-1", "cp1252"]:
            try:
                df = pd.read_csv(train_csv_path, encoding=encoding, low_memory=False)
                break
            except UnicodeDecodeError:
                continue

        if df is None:
            raise UnicodeDecodeError(f"Could not decode file: {train_csv_path}")

        return df

class DataIngestorFactory:
    @staticmethod
    def get_data_ingestor(file_extension: str) -> DataIngestor:
        if file_extension == ".zip":
            return ZipDataIngestor()
        raise ValueError(f"Unsupported file extension: {file_extension}")

if __name__ == "__main__":
    zip_path = os.path.join("data", "archive.zip")
    _, file_extension = os.path.splitext(zip_path)
    ingestor = DataIngestorFactory.get_data_ingestor(file_extension)
    dfs = ingestor.ingest(zip_path)