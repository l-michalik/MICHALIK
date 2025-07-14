import pickle
import math
import numpy as np
import os
import sys
from models import NN_with_EntityEmbedding

sys.setrecursionlimit(10000)

# === Konfiguracja ===
NUM_NETWORKS = 1
TRAIN_RATIO = 0.97
MODEL_PATH = 'pickles/models.pickle'
PREDICTION_PATH = 'predictions/predictions.csv'
TRAIN_DATA_PATH = 'pickles/feature_train_data.pickle'
TEST_DATA_PATH = 'pickles/feature_test_data.pickle'

# === Załaduj dane treningowe ===
def load_train_data():
    with open(TRAIN_DATA_PATH, 'rb') as f:
        X, y = pickle.load(f)
    return X, y

# === Trenuj modele ===
def train_models(X, y, num_networks: int, train_ratio: float):
    print("Training models...")
    models = []
    for _ in range(num_networks):
        model = NN_with_EntityEmbedding(train_ratio)
        model.fit(X, y)
        models.append(model)
    return models

# === Ewaluacja modeli ===
def evaluate_models(models, X, y):
    model0 = models[0]
    total_sqe = 0
    count = 0

    if model0.train_ratio == 1:
        return 0.0

    for i in range(model0.train_size, len(y)):
        true_sales = y[i]
        if true_sales == 0:
            continue
        prediction = np.mean([m.guess(X[i]) for m in models])
        error = ((true_sales - prediction) / true_sales) ** 2
        total_sqe += error
        count += 1

        if count % 1000 == 0:
            print(f"Evaluated {count} records — true: {true_sales}, predicted: {prediction:.2f}")

    return math.sqrt(total_sqe / count) if count else float('inf')

# === Zapisz modele ===
def save_models(models):
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(models, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Models saved to {MODEL_PATH}")

# === Załaduj dane testowe ===
def load_test_data():
    with open(TEST_DATA_PATH, 'rb') as f:
        return pickle.load(f)

# === Zapisz predykcje do CSV ===
def save_predictions(models, test_X):
    os.makedirs(os.path.dirname(PREDICTION_PATH), exist_ok=True)
    with open(PREDICTION_PATH, 'w') as f:
        f.write("Id,Sales\n")
        for i, record in enumerate(test_X):
            is_open = record[0]
            prediction = np.mean([m.guess(record) for m in models]) if is_open else 0
            f.write(f"{i + 1},{prediction:.2f}\n")
    print(f"Predictions saved to {PREDICTION_PATH}")

# === Main ===
def main():
    X, y = load_train_data()
    models = train_models(X, y, NUM_NETWORKS, TRAIN_RATIO)
    save_models(models)

    print("Evaluating ensemble...")
    rmse = evaluate_models(models, X, y)
    print(f"RMSE: {rmse:.4f}")

    test_X = load_test_data()
    save_predictions(models, test_X)

if __name__ == '__main__':
    main()
