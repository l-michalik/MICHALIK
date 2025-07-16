import math
from pathlib import Path
from typing import List, Tuple, Union
import numpy as np
import joblib
from v3.models.main import NN_with_EntityEmbedding
import sys
from pathlib import Path
from v3.config import Config
import time
import threading
from v3.utils.main import save_joblib

JOBLIB_DIR = Config.JOBLIB_DIR
CSV_DIR = Config.CSV_DIR

TRAIN_RATIO = 0.00003

sys.setrecursionlimit(10000)

def load_dataset(path: Path) -> Union[Tuple[List, List], List]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return joblib.load(path)

def save_model_ensemble(models: List[NN_with_EntityEmbedding], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(models, path)

def train_model_ensemble(
    X: List[List[float]],
    y: List[float],
    train_ratio: float
) -> List[NN_with_EntityEmbedding]:
    model = NN_with_EntityEmbedding(train_ratio)
    model.fit()
    return [model]

def evaluate_ensemble_rmse(
    models: List[NN_with_EntityEmbedding],
    X: List[List[float]],
    y: List[float],
    verbose: bool = True
) -> float:
    model0 = models[0]
    if model0.train_ratio == 1:
        return 0.0

    total_sqe = 0.0
    count = 0

    for i in range(model0.train_size, len(y)):
        true_sales = y[i]
        if true_sales == 0:
            continue

        prediction = np.mean([m.guess(X[i]) for m in models])
        error = ((true_sales - prediction) / true_sales) ** 2
        total_sqe += error
        count += 1

        if verbose and count % 1000 == 0:
            print(f"[Eval] {count} samples — True: {true_sales}, Predicted: {prediction:.2f}")

    return math.sqrt(total_sqe / count) if count else float('inf')

def write_submission_csv(
    models: List[NN_with_EntityEmbedding],
    test_features: List[List[float]],
    output_file: Path
) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open('w') as f:
        f.write("Id,Sales\n")
        for i, record in enumerate(test_features):
            is_open = record[0]
            prediction = np.mean([m.guess(record) for m in models]) if is_open else 0
            f.write(f"{i + 1},{prediction:.2f}\n")

def main():
    X, y = load_dataset(JOBLIB_DIR / "feature_train_data.joblib")
    models = train_model_ensemble(X, y, TRAIN_RATIO)
    save_joblib(models, JOBLIB_DIR / "model.joblib")

    print("Evaluating model ensemble...")
    rmse = evaluate_ensemble_rmse(models, X, y)
    print(f"RMSE: {rmse:.4f}")

    test_X = load_dataset(JOBLIB_DIR / "feature_test_data.joblib")
    write_submission_csv(models, test_X, CSV_DIR / "predictions.csv")
    print(f"Submission saved to {CSV_DIR / "predictions.csv"}")

if __name__ == '__main__':
    main()
