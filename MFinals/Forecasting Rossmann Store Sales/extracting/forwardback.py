import logging
from pathlib import Path
from typing import Tuple, Dict, List
import pandas as pd
import numpy as np
from joblib import dump
import time

from config import Config
from utils.main import save_joblib, read_csv_file

CSV_DIR = Config.CSV_DIR
JOBLIB_DIR = Config.JOBLIB_DIR

logger = logging.getLogger(__name__)

class SmartTimestampAccessor:
    def __init__(self, timestamps: np.ndarray):
        self.timestamps = timestamps
        self._last_index = 0

    def compute_index_of_timestamp(self, timestamp: np.datetime64) -> int:
        if timestamp <= self.timestamps[0]:
            return 0
        if timestamp >= self.timestamps[-1]:
            return len(self.timestamps) - 1

        while self._last_index < len(self.timestamps) - 1 and self.timestamps[self._last_index] < timestamp:
            self._last_index += 1
        while self._last_index > 0 and self.timestamps[self._last_index] > timestamp:
            self._last_index -= 1
        return self._last_index

    def get_start_end_timestamp(self) -> Tuple[np.datetime64, np.datetime64]:
        return self.timestamps[0], self.timestamps[-1]

def generate_forward_backward_matrix(csv_path: str, window_size: int = 14) -> np.ndarray:
    df = read_csv_file(csv_path)
    columns = ["Promo", "StateHoliday", "SchoolHoliday"]
    values = df[columns].to_numpy()
    n_obs, n_cols = values.shape
    features = []

    for offset in range(-window_size, window_size + 1):
        if offset == 0:
            continue
        rolled = np.roll(values, offset, axis=0)

        if offset < 0:
            rolled[offset:, :] = values[-1, :]
        else:
            rolled[:offset, :] = values[0, :]

        for col in range(n_cols):
            features.append(rolled[:, col])

    return np.array(features).T

def generate_features_for_store(
    data: pd.DataFrame,
    store_id: int,
    window_size: int = 14,
    only_zero: bool = False
) -> Tuple[np.ndarray, List[str]]:
    store_data = data[data["Store"] == store_id]
    columns = ["Promo", "StateHoliday", "SchoolHoliday"]
    column_data = store_data[columns].astype(str).to_numpy()[::-1]
    timestamps = pd.to_datetime(store_data["Date"]).dt.floor("D").to_numpy()[::-1]


    feature_names = ["Date", "Store"]
    data_rows = [timestamps.tolist(), [store_id] * len(store_data)]

    for i_col, column in enumerate(columns):
        unique_vals = {"0"} if only_zero else set(store_data[column].astype(str))
        for val in unique_vals:
            fw_first, bw_last, fw_count, bw_count = [], [], [], []
            fw_ts = SmartTimestampAccessor(timestamps)
            bw_ts = SmartTimestampAccessor(timestamps)

            for i in range(len(column_data)):
                ts = timestamps[i]
                ts_fwd = ts + np.timedelta64(window_size, "D")
                ts_bwd = ts - np.timedelta64(window_size, "D")
                i_fwd = fw_ts.compute_index_of_timestamp(ts_fwd)
                i_bwd = bw_ts.compute_index_of_timestamp(ts_bwd)

                if i == len(column_data) - 1:
                    fw_first.append(window_size + 1)
                    fw_count.append(0)
                else:
                    fwd_slice = column_data[i + 1:i_fwd + 1, i_col] != val
                    fw_first.append(np.argmax(fwd_slice) + 1 if np.any(fwd_slice) else window_size + 1)
                    fw_count.append(np.sum(fwd_slice))

                if i == 0:
                    bw_last.append(window_size + 1)
                    bw_count.append(0)
                else:
                    bwd_slice = column_data[i_bwd:i, i_col] != val
                    bw_last.append(np.argmax(bwd_slice[::-1]) + 1 if np.any(bwd_slice) else window_size + 1)
                    bw_count.append(np.sum(bwd_slice))

            data_rows.extend([fw_first, bw_last])
            feature_names.extend([
                f"{column}_first_forward_looking",
                f"{column}_last_backward_looking"
            ])

            if column == "StateHoliday":
                data_rows.extend([fw_count, bw_count])
                feature_names.extend([
                    f"{column}_count_forward_looking",
                    f"{column}_count_backward_looking"
                ])

    return np.array(data_rows).T, feature_names

def extract_forwardback(window_size: int = 7) -> None:
    train_df = read_csv_file(CSV_DIR / "rossmann-store-sales/train.csv")
    test_df = read_csv_file(CSV_DIR / "rossmann-store-sales/test.csv")
    store_ids = np.unique(train_df["Store"])

    fb_dict: Dict[Tuple[int, np.datetime64], np.ndarray] = {}
    output_path = JOBLIB_DIR / "forwardback.joblib"

    for source_name, df in [("train", train_df), ("test", test_df)]:
        start_time = time.time()
        last_log_time = start_time
        total = len(store_ids)

        for i, store_id in enumerate(store_ids, start=1):
            rows, feature_names = generate_features_for_store(df, store_id, window_size=window_size, only_zero=True)
            date_idx = feature_names.index("Date")
            for row in rows:
                key = (store_id, row[date_idx])
                fb_dict[key] = row[2:]

            now = time.time()
            if now - last_log_time >= 5:
                percent = (i / total) * 100
                logger.info(f"{source_name}: {i}/{total} stores processed ({percent:.1f}%)")
                print(f"...({percent:.1f}%)")
                last_log_time = now

        logger.info(f"Processed {source_name} features for {total} stores")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_joblib(fb_dict, output_path)
    logger.info(f"Saved forward/backward features to {output_path}")

if __name__ == "__main__":
    extract_forwardback()
