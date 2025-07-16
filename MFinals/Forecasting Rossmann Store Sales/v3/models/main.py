import math
import numpy as np
from pathlib import Path
from joblib import load 
from keras.models import Model
from keras.layers import (
    Input, Embedding, Dense, Dropout, Reshape, Concatenate
)
from keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler
from v3.utils.main import split_features
from v3.config import Config

JOBLIB_DIR = Config.JOBLIB_DIR

class ModelBase:
    def __init__(self, train_ratio: float):
        self.train_ratio = train_ratio
        self._load_data()

    def _load_data(self):
        X, y = load(JOBLIB_DIR / "feature_train_data.joblib")
        self.X = np.array(X)
        self.y = np.array(y)

        self.num_records = len(self.X)
        self.train_size = int(self.train_ratio * self.num_records)

        self.X_val = self.X[self.train_size:]
        self.y_val = self.y[self.train_size:]
        self.X = self.X[:self.train_size]
        self.y = self.y[:self.train_size]

    def evaluate(self, batch_size: int = 512):
        if self.train_ratio == 1:
                return 0.0

        X_val_processed = self._preprocess(self.X_val)
        preds = self.model.predict(X_val_processed, batch_size=batch_size, verbose=0)
        preds = self._val_for_pred(preds).flatten()

        non_zero_mask = self.y_val != 0
        y_val_filtered = self.y_val[non_zero_mask]
        preds_filtered = preds[non_zero_mask]

        error = ((y_val_filtered - preds_filtered) / y_val_filtered) ** 2
        return np.sqrt(np.mean(error)) if len(error) else float('inf')


class NN_with_EntityEmbedding(ModelBase):
    def __init__(self, train_ratio: float):
        super().__init__(train_ratio)
        self.nb_epochs = 20
        self.batch_size = 128
        self.max_log_y = np.max(np.log(self.y))

        self._build_preprocessors()
        self._build_model()
        self.fit()

    def _build_preprocessors(self):
        X_list = split_features(self.X)
        self.scalers = {
            32: StandardScaler().fit(X_list[32]),
            33: StandardScaler().fit(X_list[33])
        }

    def _preprocess(self, X: np.ndarray):
        X_list = split_features(X)
        for idx, scaler in self.scalers.items():
            X_list[idx] = scaler.transform(X_list[idx])
        return X_list

    def _build_model(self):
        inputs, embeddings = [], []

        def embed(name, input_dim, output_dim):
            inp = Input(shape=(1,), name=name)
            emb = Embedding(input_dim, output_dim)(inp)
            inputs.append(inp)
            embeddings.append(Reshape((output_dim,))(emb))

        def dense(name, dim):
            inp = Input(shape=(dim,), name=name)
            inputs.append(inp)
            embeddings.append(inp)

        embed("store", 1115, 50)
        embed("day_of_week", 7, 6)
        dense("promo", 1)
        embed("year", 3, 2)
        embed("month", 12, 6)
        embed("day", 31, 10)
        embed("state_holiday", 4, 3)
        dense("school_holiday", 1)
        embed("comp_months", 25, 2)
        embed("promo2weeks", 26, 1)
        embed("latest_promo2", 4, 1)
        dense("distance", 1)
        embed("store_type", 5, 2)
        embed("assortment", 4, 3)
        embed("promo_interval", 4, 3)
        embed("comp_year", 18, 4)
        embed("promo2_year", 8, 4)
        embed("state", 12, 6)
        embed("week_of_year", 53, 2)

        dense("temperature", 3)
        dense("humidity", 3)
        dense("wind", 2)
        dense("cloud", 1)
        embed("weather_event", 22, 4)

        embed("promo_forward", 8, 1)
        embed("promo_backward", 8, 1)
        embed("stateholiday_forward", 8, 1)
        embed("stateholiday_backward", 8, 1)
        embed("stateholiday_count_forward", 3, 1)
        embed("stateholiday_count_backward", 3, 1)
        embed("school_forward", 8, 1)
        embed("school_backward", 8, 1)

        dense("trend_de", 1)
        dense("trend_state", 1)

        x = Dropout(0.02)(Concatenate()(embeddings))
        x = Dense(1000, kernel_initializer="uniform", activation="relu")(x)
        x = Dense(500, kernel_initializer="uniform", activation="relu")(x)
        x = Dense(1, activation="sigmoid")(x)

        self.model = Model(inputs=inputs, outputs=x)
        self.model.compile(optimizer=Adam(), loss="mean_absolute_error")

    def _val_for_fit(self, y):
        return np.log(y) / self.max_log_y

    def _val_for_pred(self, y):
        return np.exp(y * self.max_log_y)

    def fit(self):
        X_train = self._preprocess(self.X)
        y_train = self._val_for_fit(self.y)

        if self.train_ratio < 1:
            X_val = self._preprocess(self.X_val)
            y_val = self._val_for_fit(self.y_val)
            self.model.fit(X_train, y_train,
                           validation_data=(X_val, y_val),
                           epochs=self.nb_epochs,
                           batch_size=self.batch_size,
                           verbose=1)
            print("Validation RMSE:", self.evaluate())
        else:
            self.model.fit(X_train, y_train,
                           epochs=self.nb_epochs,
                           batch_size=self.batch_size,
                           verbose=1)

    def guess(self, x):
        x_processed = self._preprocess(np.array(x).reshape(1, -1))
        pred = self.model.predict(x_processed, verbose=0)
        return self._val_for_pred(pred)[0][0]