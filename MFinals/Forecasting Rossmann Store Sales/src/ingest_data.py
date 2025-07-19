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

        csv_files = []
        for root, _, files in os.walk(extract_dir):
            for f in files:
                if f.endswith(".csv"):
                    csv_files.append(os.path.join(root, f))

        if not csv_files:
            raise FileNotFoundError("No CSV files found")

        dataframes = []
        for path in csv_files:
            df = pd.read_csv(path)
            dataframes.append(df)

        print(f"Extracted {len(dataframes)} CSV files")

        return dataframes

class DataIngestorFactory:
    @staticmethod
    def get_data_ingestor(file_extension: str) -> DataIngestor:
        if file_extension == ".zip":
            return ZipDataIngestor()
        raise ValueError(f"Unsupported file extension: {file_extension}")

if __name__ == "__main__":
    zip_path = os.path.join("extracted_data", "archive.zip")
    _, file_extension = os.path.splitext(zip_path)
    ingestor = DataIngestorFactory.get_data_ingestor(file_extension)
    dfs = ingestor.ingest(zip_path)