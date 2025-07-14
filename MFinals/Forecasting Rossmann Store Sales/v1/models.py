import pickle
import math
import numpy as np

from sklearn.preprocessing import StandardScaler
from keras.models import Model
from keras.layers import (
    Input, Embedding, Dense, Dropout, Activation, Reshape, Concatenate
)
from keras.optimizers import Adam
from prepare_nn_features import split_features

class ModelBase:
    def __init__(self, train_ratio: float):
        self.train_ratio = train_ratio
        self._load_data()

    def _load_data(self):
        with open('pickles/feature_train_data.pickle', 'rb') as f:
            self.X, self.y = pickle.load(f)

        self.X = np.array(self.X)
        self.y = np.array(self.y)

        self.num_records = len(self.X)
        self.train_size = int(self.train_ratio * self.num_records)

        self.X_val = self.X[self.train_size:]
        self.y_val = self.y[self.train_size:]
        self.X = self.X[:self.train_size]
        self.y = self.y[:self.train_size]

    def evaluate(self):
        if self.train_ratio == 1:
            return 0
        total_sqe = 0
        count = 0
        for x, true_y in zip(self.X_val, self.y_val):
            if true_y == 0:
                continue
            pred = self.guess(x)
            total_sqe += ((true_y - pred) / true_y) ** 2
            count += 1
        return math.sqrt(total_sqe / count) if count else float('inf')


class NN_with_EntityEmbedding(ModelBase):
    def __init__(self, train_ratio: float):
        super().__init__(train_ratio)

        self.nb_epochs = 20
        self.batch_size = 128
        self.max_log_y = np.max(np.log(self.y))
        self.min_log_y = np.min(np.log(self.y))

        self._build_preprocessors(self.X)
        self._build_model()
        self.fit()

    def _build_preprocessors(self, X):
        X_list = split_features(X)
        self.gt_de_enc = StandardScaler().fit(X_list[32])
        self.gt_state_enc = StandardScaler().fit(X_list[33])

    def _preprocess(self, X):
        X_list = split_features(X)
        X_list[32] = self.gt_de_enc.transform(X_list[32])
        X_list[33] = self.gt_state_enc.transform(X_list[33])
        return X_list

    def _build_model(self):
        inputs = []
        embeddings = []

        def embed_input(name, input_dim, output_dim):
            inp = Input(shape=(1,), name=name)
            emb = Embedding(input_dim, output_dim)(inp)
            emb = Reshape(target_shape=(output_dim,))(emb)
            inputs.append(inp)
            embeddings.append(emb)

        def dense_input(name, dim):
            inp = Input(shape=(dim,), name=name)
            inputs.append(inp)
            embeddings.append(inp)

        # Embed categorical features
        embed_input("store", 1115, 50)
        embed_input("day_of_week", 7, 6)
        dense_input("promo", 1)
        embed_input("year", 3, 2)
        embed_input("month", 12, 6)
        embed_input("day", 31, 10)
        embed_input("state_holiday", 4, 3)
        dense_input("school_holiday", 1)
        embed_input("comp_months", 25, 2)
        embed_input("promo2weeks", 26, 1)
        embed_input("latest_promo2", 4, 1)
        dense_input("distance", 1)
        embed_input("store_type", 5, 2)
        embed_input("assortment", 4, 3)
        embed_input("promo_interval", 4, 3)
        embed_input("comp_year", 18, 4)
        embed_input("promo2_year", 8, 4)
        embed_input("state", 12, 6)
        embed_input("week_of_year", 53, 2)

        # Dense weather / trend features
        dense_input("temperature", 3)
        dense_input("humidity", 3)
        dense_input("wind", 2)
        dense_input("cloud", 1)
        embed_input("weather_event", 22, 4)

        embed_input("promo_forward", 8, 1)
        embed_input("promo_backward", 8, 1)
        embed_input("stateholiday_forward", 8, 1)
        embed_input("stateholiday_backward", 8, 1)
        embed_input("stateholiday_count_forward", 3, 1)
        embed_input("stateholiday_count_backward", 3, 1)
        embed_input("school_forward", 8, 1)
        embed_input("school_backward", 8, 1)

        dense_input("trend_de", 1)
        dense_input("trend_state", 1)

        merged = Concatenate()(embeddings)

        x = Dropout(0.02)(merged)
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
        x_arr = np.array(x).reshape(1, -1)
        x_processed = self._preprocess(x_arr)
        pred = self.model.predict(x_processed, verbose=0)
        return self._val_for_pred(pred)[0][0]
