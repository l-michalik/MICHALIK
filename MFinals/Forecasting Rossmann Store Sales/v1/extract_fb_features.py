import numpy as np
import pandas as pd
import pickle
import os

class SmartTimestampAccessor:
    def __init__(self, timestamps):
        self.timestamps = timestamps
        self._last_index = 0

    def compute_index_of_timestamp(self, timestamp):
        if timestamp <= self.timestamps[0]:
            return 0
        if timestamp >= self.timestamps[-1]:
            return len(self.timestamps) - 1

        while self._last_index < len(self.timestamps) - 1 and self.timestamps[self._last_index] < timestamp:
            self._last_index += 1
        while self._last_index > 0 and self.timestamps[self._last_index] > timestamp:
            self._last_index -= 1
        return self._last_index

    def get_start_end_timestamp(self):
        return self.timestamps[0], self.timestamps[-1]

def generate_forward_backward_matrix(csv_path, window_size=14):
    df = pd.read_csv(csv_path)
    columns = ["Promo", "StateHoliday", "SchoolHoliday"]
    values = np.array(df[columns])
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

def generate_features_for_store(data, store_id, window_size=14, only_zero=False):
    store_data = data[data["Store"] == store_id]
    columns = ["Promo", "StateHoliday", "SchoolHoliday"]
    column_data = np.array(store_data[columns], dtype=str)[::-1]
    timestamps = np.array(store_data["Date"], dtype="datetime64[D]")[::-1]

    feature_names = ["Date", "Store"]
    data_rows = [store_data["Date"][::-1].tolist(), [store_id] * len(store_data)]

    for i_col, column in enumerate(columns):
        unique_vals = {"0"} if only_zero else set(store_data[column].astype(str))
        for val in unique_vals:
            fw_first, bw_last = [], []
            fw_count, bw_count = [], []
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

            data_rows.append(fw_first)
            data_rows.append(bw_last)
            feature_names.append(f"{column}_first_forward_looking")
            feature_names.append(f"{column}_last_backward_looking")

            if column == "StateHoliday":
                data_rows.append(fw_count)
                data_rows.append(bw_count)
                feature_names.append(f"{column}_count_forward_looking")
                feature_names.append(f"{column}_count_backward_looking")

    return np.array(data_rows).T, feature_names

def generate_all_fb_features(train_path="./extracted/train.csv", test_path="./extracted/test.csv", output_path="./pickles/fb.pickle"):
    train_df = pd.read_csv(train_path, low_memory=False)
    test_df = pd.read_csv(test_path, low_memory=False)
    store_ids = np.unique(train_df["Store"])

    fb_dict = {}

    for store_id in store_ids:
        feature_names, names = generate_features_for_store(train_df, store_id, window_size=7, only_zero=True)
        print(names)
        date_idx = names.index("Date")
        for row in feature_names:
            key = (store_id, row[date_idx])
            fb_dict[key] = row[2:]

    print("Generating forward-backward features for TEST set...")
    for store_id in store_ids:
        feature_names, names = generate_features_for_store(test_df, store_id, window_size=7, only_zero=True)
        date_idx = names.index("Date")
        for row in feature_names:
            key = (store_id, row[date_idx])
            fb_dict[key] = row[2:]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        pickle.dump(fb_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

    return fb_dict

if __name__ == "__main__":
    generate_all_fb_features()
